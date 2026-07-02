"""Agente Gerador (A1) — produz casos de teste de sistema a partir de user story + RAG."""
from google.adk.agents import LlmAgent
from src.model_backends import get_model
from src.tools.retriever import recuperar_contexto
from src.config import PROMPTS_DIR

_PROMPT = (PROMPTS_DIR / "a1_gerador.md").read_text(encoding="utf-8")


def build_a1() -> LlmAgent:
    return LlmAgent(
        name="a1_gerador",
        model=get_model("a1_gerador"),
        instruction=_PROMPT,
        tools=[recuperar_contexto],
        output_key="casos_atuais",
    )
