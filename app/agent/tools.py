import re
import pandas as pd
from app.agent.schema import TextToSQLDeps
from pydantic_ai import RunContext

from agent import sql_agent
from db import get_connection
from utils import get_tabelas_validas

def get_tabelas(conn) -> set:
    return get_tabelas_validas(conn)

def validar_sql(sql: str, TABELAS_VALIDAS: set) -> str:
    '''Guardrail para validar a consulta SQL antes de executá-la.'''

    sql = sql.strip()

    sql = re.sub(r"--.*", "", sql)
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)

    sql = sql.strip()
    sql_upper = sql.upper()

    if not sql_upper.startswith("SELECT"):
        raise ValueError("Apenas SELECT permitido")

    proibidos = ["DELETE", "UPDATE", "INSERT", "DROP", "ALTER", "PRAGMA"]
    if any(p in sql_upper for p in proibidos):
        raise ValueError("Operação não permitida")

    if ";" in sql[:-1]:
        raise ValueError("Múltiplas queries não permitidas")

    tabelas_encontradas = set(
        re.findall(r"\b(?:FROM|JOIN)\s+\"?([a-zA-Z_][a-zA-Z0-9_]*)\"?", sql, re.IGNORECASE)
    )

    tabelas_invalidas = tabelas_encontradas - TABELAS_VALIDAS

    if tabelas_invalidas:
        raise ValueError(f"Tabelas não permitidas: {tabelas_invalidas}")

    if "LIMIT" not in sql_upper:
        sql = sql.rstrip(";") + " LIMIT 50"

    return sql

@sql_agent.tool
def get_table_info(ctx: RunContext[TextToSQLDeps], table_name: str) -> str:
    """Busca a declaração CREATE TABLE e as primeiras 3 linhas de amostra para uma tabela dada.
    Use isso para entender o esquema das tabelas relevantes."""

    conn = get_connection()
    tabelas_validas = get_tabelas_validas(conn)
    if table_name not in tabelas_validas:
        conn.close()
        return f"Error: Tabela inválida '{table_name}'. Verifique o esquema e tente novamente."

    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return f"Tabela '{table_name}' não encontrada. Verifique o esquema."
    schema_sql = row[0]
    df = pd.read_sql_query(f"SELECT * FROM [{table_name}] LIMIT 3", conn)
    conn.close()
    return f"{schema_sql}\n\nSample rows:\n{df.to_string(index=False)}"


@sql_agent.tool
def get_distinct_values(ctx: RunContext[TextToSQLDeps], table_name: str, column_name: str) -> str:
    """Busque até 20 valores distintos para uma coluna específica. Use isso para verificar os valores reais no banco de dados,
    o que pode ajudar a evitar erros de filtro e JOIN."""
    
    conn = get_connection()

    tabelas_validas = get_tabelas_validas(conn)
    if table_name not in tabelas_validas:
        conn.close()
        return f"Error: Tabela inválida '{table_name}'. Verifique o esquema e tente novamente."

    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT [{column_name}] FROM [{table_name}] LIMIT 20")
        values = [str(row[0]) for row in cursor.fetchall()]
        return f"Valores distintos em {table_name}.{column_name}: {values}"
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()


@sql_agent.tool
def execute_query(ctx: RunContext[TextToSQLDeps], sql_query: str) -> str:
    """Execute a consulta SQL e retorne os resultados. Use isso para testar seu SQL antes de retorná-lo como resposta final."""

    conn = get_connection()
    TABELAS_VALIDAS = get_tabelas_validas(conn)
    try:
        sql_query = validar_sql(sql_query, TABELAS_VALIDAS)
    except Exception as e:
        return f"Query bloqueada: {e}"

    try:
        df = pd.read_sql_query(sql_query, conn)
        if df.empty:
            return "Query retornou 0 linhas. Pode ser correto (resultado vazio) ou ter um erro lógico."
        return f"Query returnou {len(df)} linhas:\n{df.to_string(index=False)}"
    except Exception as e:
        return f"SQL Error: {e}. Conserte a query e tente novamente."
    finally:
        conn.close()