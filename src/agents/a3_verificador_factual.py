"""
Agente Verificador Factual (A3).

Mitiga alucinação de domínio (Incorrect Fact de Silva et al., 2026;
reliability gap de Gheventer et al., 2026) ancorando cada caso em evidência
recuperada do código-fonte e documentação do monitoria-app.
"""
from pathlib import Path
from google.adk.agents import LlmAgent
from src.model_backends import get_model
from src.tools.retriever import recuperar_contexto
from src.tools.exit_tools import exit_loop
from src.config import PROMPTS_DIR

_PROMPT = (PROMPTS_DIR / "a3_verificador_factual.md").read_text(encoding="utf-8")


def build_a3() -> LlmAgent:
    return LlmAgent(
        name="a3_verificador_factual",
        model=get_model("a3_verificador_factual"),
        instruction=_PROMPT,
        tools=[recuperar_contexto, exit_loop],
        output_key="relatorio_factual",
    )
