"""
Backend determinístico de fixtures para MODEL_BACKEND=dryrun.

Produz Markdown estruturado (não JSON) correspondendo ao novo formato
de saída dos agentes. Respostas intencionalmente simples — nunca devem
ser confundidas com resultados experimentais reais.

Todo registro gerado neste modo inclui "modo": "dry_run".
Tokens/latência/custo registrados como zero.
"""
from __future__ import annotations

from typing import AsyncGenerator

import google.genai.types as genai_types
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

_DRY_RUN_CASO = """\
### US00-CT01 — [dry_run] Caso de teste fictício
- **Pré-condição:** Usuário autenticado
- **Objetivo:** Validar fluxo principal
- **Resultado esperado:** Sistema processa e retorna sucesso
- **Tipo:** principal
- **Critérios cobertos:** dry_run
- **Verificação:** NAO_VERIFICAVEL — evidência: dry_run — fonte: dry_run (tipo: código)
- **Origem:** A1
- **Aprovado humano:** pendente
"""

_DRY_RUN_LACUNAS = """\
## Lacunas identificadas
_Nenhuma lacuna identificada nesta rodada._
"""

_DRY_RUN_FACTUAL = """\
## Verificação factual
### US00-CT01
- **Status:** NAO_VERIFICAVEL
- **Evidência:** [dry_run] Sem verificações reais.
- **Fonte:** dry_run (tipo: código)
"""


class DryRunModel(BaseLlm):
    """Modelo fixture determinístico para testes de arquitetura sem chamadas de API."""

    agent_role: str = "unknown"

    @classmethod
    def supported_models(cls) -> list[str]:
        return [r"dryrun/.*"]

    async def generate_content_async(
        self,
        llm_request: LlmRequest,
        stream: bool = False,
    ) -> AsyncGenerator[LlmResponse, None]:
        text = self._build_response()
        content = genai_types.Content(
            parts=[genai_types.Part(text=text)],
            role="model",
        )
        yield LlmResponse(content=content, partial=False, turn_complete=True)

    def _build_response(self) -> str:
        role = self.agent_role
        if role == "a2_critico_cobertura":
            return _DRY_RUN_LACUNAS
        if role == "a3_verificador_factual":
            return _DRY_RUN_FACTUAL
        # a1_gerador, a4_curador, zero_shot — todos retornam Markdown de casos
        return _DRY_RUN_CASO
