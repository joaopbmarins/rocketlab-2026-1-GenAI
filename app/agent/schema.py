from dataclasses import dataclass
from pydantic import BaseModel, Field

@dataclass
class TextToSQLDeps:
    """Dependências necessárias para o processo de text-to-SQL com schema linking."""
    schema: str


class SQLResult(BaseModel):
    """Saída estruturada do agente de text-to-SQL."""
    reasoning: str = Field(description="Racional para a construção da consulta SQL")
    sql: str = Field(description="Query SQL final")
    confidence: str = Field(
        description="Nível de confiança: 'high' se testado e verificado, 'medium' se não testado, 'low' se incerto"
    )