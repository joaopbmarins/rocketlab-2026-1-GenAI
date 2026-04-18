import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from app.agent.schema import TextToSQLDeps, SQLResult
from app.utils import get_schema
from app.prompt import SYSTEM_PROMPT

from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
MODEL = "gemini-2.5-flash-lite"

# Instanciando Provider e Modelo
provider = GoogleProvider(api_key=GOOGLE_API_KEY)
pydantic_model = GoogleModel(MODEL, provider=provider)

sql_agent = Agent(
    pydantic_model,
    deps_type=TextToSQLDeps,
    output_type=SQLResult,
    instructions=SYSTEM_PROMPT,
    retries=2,
)

deps = TextToSQLDeps(schema=get_schema())

def run_sql_agent(question: str) -> SQLResult:
    """Executa o agente de text-to-SQL com linking, passando as dependências necessárias.
    O agente usará as ferramentas para iterar e refinar seu SQL até chegar a uma resposta final testada."""

    user_msg = f"""Visão geral do esquema do banco de dados:
{deps.schema}

Pergunta: {question}"""
    
    result = sql_agent.run_sync(user_msg, deps=deps)
    return result.output