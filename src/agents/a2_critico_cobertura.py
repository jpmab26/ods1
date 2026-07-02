"""
Agente Crítico de Cobertura (A2).

Ataca a omissão sistemática de cenários implícitos identificada por
Silva et al. (2026) como falha dominante (508–543 falsos negativos).
"""
from pathlib import Path
from google.adk.agents import LlmAgent
from src.model_backends import get_model
from src.tools.retriever import recuperar_contexto
from src.tools.exit_tools import exit_loop
from src.config import PROMPTS_DIR

_PROMPT = (PROMPTS_DIR / "a2_critico_cobertura.md").read_text(encoding="utf-8")


def build_a2() -> LlmAgent:
    return LlmAgent(
        name="a2_critico_cobertura",
        model=get_model("a2_critico_cobertura"),
        instruction=_PROMPT,
        tools=[recuperar_contexto, exit_loop],
        output_key="critica_cobertura",
    )
