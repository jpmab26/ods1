from typing import Literal
from pydantic import BaseModel


class Verificacao(BaseModel):
    status: Literal["SUPORTADO", "NAO_SUPORTADO", "NAO_VERIFICAVEL"]
    evidencia: str
    fonte: str


class CasoDeTeste(BaseModel):
    id: str
    nome: str
    pre_condicao: str
    objetivo: str
    resultado_esperado: str
    tipo: Literal["principal", "alternativo", "borda", "erro"]
    criterios_cobertos: list[str]
    # Ausente em T0 (sem A3); tratado como NAO_VERIFICAVEL implícito em eval/metrics.py
    # conforme nota do Apêndice B do plano.
    verificacao: Verificacao | None = None
    origem: list[str] = []
    aprovado_humano: bool | None = None


class Lacuna(BaseModel):
    descricao: str
    tipo: Literal["alternativo", "borda", "erro"]
    justificativa: str


class RelatorioCobertura(BaseModel):
    lacunas: list[Lacuna]


class VerificacaoItem(BaseModel):
    id_caso: str
    status: Literal["SUPORTADO", "NAO_SUPORTADO", "NAO_VERIFICAVEL"]
    evidencia: str
    fonte: str


class RelatorioFactual(BaseModel):
    verificacoes: list[VerificacaoItem]
    relatorio_factual: str
