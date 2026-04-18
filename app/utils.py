import pandas as pd
import re
from app.db import get_connection

def get_schema() -> str:
    """Extrair scripts DDL de todas as tabelas do banco de dados e retornar como string formatada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL;")
    schemas = [row[0] for row in cursor.fetchall()]
    conn.close()
    return "\n\n".join(schemas)


def get_sample_rows(table: str, n: int = 3) -> str:
    """Retornar as primeiras n linhas de uma tabela como string formatada."""
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT {n}", conn)
    conn.close()
    return df.to_string(index=False)


def execute_sql(sql: str) -> pd.DataFrame:
    """Executa a consulta SQL e retorna os resultados como DataFrame."""
    conn = get_connection()
    try:
        df = pd.read_sql_query(sql, conn)
        return df
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})
    finally:
        conn.close()


def extract_sql(text: str) -> str:
    """Extrai o código SQL de uma string, procurando por blocos de código ou SELECT."""
    match = re.search(r'```(?:sql)?\s*\n?(.*?)\n?```', text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r'((?:SELECT)\b.*?;)', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def get_tabelas_validas(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    tabelas = [row[0] for row in cursor.fetchall()]
    return set(tabelas)