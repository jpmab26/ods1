"""
Seletor de backend de modelo por MODEL_BACKEND ∈ {gemini, gemini_flash, nvidia, nvidia_super, openai_oss, dryrun}.

IDs de modelo verificados em 29/06/2026 — confirmar na documentação do provedor
antes de usar em produção:
  - Gemini: https://ai.google.dev/gemini-api/docs/models
  - OpenRouter (NVIDIA/OpenAI): https://openrouter.ai/models

Backends disponíveis
--------------------
  gemini       → gemini-2.5-flash-lite                              (Google AI Studio, GOOGLE_API_KEY)
  gemini_flash → gemini-2.5-flash                                   (Google AI Studio, GOOGLE_API_KEY) — T0 only
  nvidia       → nvidia/nemotron-3-ultra-550b-a55b:free             (OpenRouter via LiteLLM, OPENROUTER_API_KEY) — T0 only
  nvidia_super → nvidia/nemotron-3-super-120b-a12b:free             (OpenRouter via LiteLLM, OPENROUTER_API_KEY)
  openai_oss   → openai/gpt-oss-120b:free                           (OpenRouter via LiteLLM, OPENROUTER_API_KEY)
  dryrun       → DryRunModel                                        (sem chamadas de API, para smoke tests)
"""
import os

# Identificadores canônicos — abstraídos para facilitar migração quando
# um modelo for descontinuado (ex.: gemini-2.5-flash-lite → gemini-3.1-flash-lite).
# Override via env var *_MODEL_ID (útil quando o modelo padrão está indisponível).
_GEMINI_MODEL_ID = os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash-lite")
_GEMINI_FLASH_MODEL_ID = os.getenv("GEMINI_FLASH_MODEL_ID", "gemini-2.5-flash")
_NVIDIA_MODEL_ID = os.getenv(
    "NVIDIA_MODEL_ID",
    "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free",
)
_NVIDIA_SUPER_MODEL_ID = os.getenv(
    "NVIDIA_SUPER_MODEL_ID",
    "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
)
_OPENAI_OSS_MODEL_ID = os.getenv(
    "OPENAI_OSS_MODEL_ID",
    "openrouter/openai/gpt-oss-120b:free",
)

_BACKEND = os.getenv("MODEL_BACKEND", "dryrun")

# Todos os backends que usam OpenRouter via LiteLLM
_OPENROUTER_BACKENDS = {
    "nvidia":       _NVIDIA_MODEL_ID,
    "nvidia_super": _NVIDIA_SUPER_MODEL_ID,
    "openai_oss":   _OPENAI_OSS_MODEL_ID,
}


def get_model(agent_role: str):
    """
    Retorna o identificador de modelo para o backend selecionado.

    Returns:
        str          — para os backends 'gemini' e 'gemini_flash'
        LiteLlm      — para os backends 'nvidia', 'nvidia_super', 'openai_oss'
        DryRunModel  — para backend 'dryrun'
    """
    backend = os.getenv("MODEL_BACKEND", _BACKEND)

    if backend == "gemini":
        return _GEMINI_MODEL_ID

    if backend == "gemini_flash":
        return _GEMINI_FLASH_MODEL_ID

    if backend in _OPENROUTER_BACKENDS:
        # Todos os modelos OpenRouter compartilham OPENROUTER_API_KEY
        from google.adk.models.lite_llm import LiteLlm
        return LiteLlm(model=_OPENROUTER_BACKENDS[backend])

    if backend == "dryrun":
        from src.dry_run import DryRunModel
        return DryRunModel(model=f"dryrun/{agent_role}", agent_role=agent_role)

    valid = "gemini, gemini_flash, nvidia, nvidia_super, openai_oss, dryrun"
    raise ValueError(f"MODEL_BACKEND inválido: '{backend}'. Use: {valid}.")
