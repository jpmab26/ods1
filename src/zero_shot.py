"""
Implementação do tratamento T0 (zero-shot): LlmAgent único, sem RAG e sem LoopAgent.

A única diferença estrutural entre T0 e T1/T2/T3 é a ausência de RAG e crítica em laço.
Mesmo T0 é instrumentado via ADK Runner para que tokens/latência sejam mensuráveis
pelo mesmo mecanismo em todos os tratamentos (Seção 5, Relatório Parcial).
"""
from google.adk.agents import LlmAgent
from src.model_backends import get_model
from src.config import PROMPTS_DIR

_PROMPT = (PROMPTS_DIR / "zero_shot.md").read_text(encoding="utf-8")


def build_zero_shot() -> LlmAgent:
    return LlmAgent(
        name="zero_shot",
        model=get_model("zero_shot"),
        instruction=_PROMPT,
        output_key="casos_atuais",
    )
