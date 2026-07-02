"""
Agente Curador (A4).

Controla a verbosidade introduzida pelo RAG (efeito colateral identificado por
Correia et al., 2025) e produz a lista final de casos prontos para revisão humana.
"""
from pathlib import Path
from google.adk.agents import LlmAgent
from src.model_backends import get_model
from src.config import PROMPTS_DIR

_PROMPT = (PROMPTS_DIR / "a4_curador.md").read_text(encoding="utf-8")


def build_a4() -> LlmAgent:
    return LlmAgent(
        name="a4_curador",
        model=get_model("a4_curador"),
        instruction=_PROMPT,
        output_key="casos_finais",
    )
