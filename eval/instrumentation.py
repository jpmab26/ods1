"""
Instrumentação centralizada de tokens, latência e custo por execução.

Preços de tabela vigentes em 29/06/2026 (confirmar antes de usar):
  - gemini-2.5-flash-lite:              US$0,10/M tokens entrada, US$0,40/M saída
  - gemini-2.5-flash:                   US$0,30/M entrada, US$2,50/M saída
  - nvidia/nemotron-3-ultra-550b-a55b:  US$0,00 (free tier OpenRouter)
  - nvidia/nemotron-3-super-120b-a12b:  US$0,00 (free tier OpenRouter)
  - openai/gpt-oss-120b:                US$0,00 (free tier OpenRouter)
"""
from __future__ import annotations

import os
from dataclasses import dataclass


_PRICES: dict[str, dict[str, float]] = {
    "gemini-2.5-flash-lite":    {"input": 0.10, "output": 0.40},
    "gemini-2.5-flash":         {"input": 0.30, "output": 2.50},
    "nvidia-nemotron-ultra":    {"input": 0.0,  "output": 0.0},
    "nvidia-nemotron-super":    {"input": 0.0,  "output": 0.0},
    "openai-gpt-oss-120b":      {"input": 0.0,  "output": 0.0},
    "dryrun":                   {"input": 0.0,  "output": 0.0},
}


@dataclass
class ExecutionRecord:
    tokens_entrada: int = 0
    tokens_saida: int = 0
    latencia_s: float = 0.0
    custo_usd: float = 0.0
    modo: str = "real"
    model_backend: str = ""
    pipeline: str = ""
    iteracoes_cobertura: int = 0
    iteracoes_factual: int = 0


def compute_cost(tokens_in: int, tokens_out: int, backend: str) -> float:
    key_map = {
        "gemini":       "gemini-2.5-flash-lite",
        "gemini_flash": "gemini-2.5-flash",
        "nvidia":       "nvidia-nemotron-ultra",
        "nvidia_super": "nvidia-nemotron-super",
        "openai_oss":   "openai-gpt-oss-120b",
    }
    key = key_map.get(backend, backend)
    prices = _PRICES.get(key, {"input": 0.0, "output": 0.0})
    return (tokens_in * prices["input"] + tokens_out * prices["output"]) / 1_000_000


def build_execution_record(
    tokens_in: int, tokens_out: int, elapsed_s: float, backend: str, pipeline: str
) -> ExecutionRecord:
    """Monta o registro de execução a partir de tokens já agregados.

    O ADK Runner expõe uso de tokens por Event (um por chamada de LLM), não
    num único "response" — para um pipeline multiagente isso significa vários
    eventos por execução (A1, A2, A1b, A3, A1c, A4...). O chamador deve somar
    prompt_token_count/candidates_token_count de todos os eventos do stream
    antes de passar para cá (ver eval/runner.py:_run_pipeline_async).
    """
    if os.getenv("MODEL_BACKEND", "dryrun") == "dryrun":
        return ExecutionRecord(modo="dry_run", model_backend=backend, pipeline=pipeline)

    return ExecutionRecord(
        tokens_entrada=tokens_in,
        tokens_saida=tokens_out,
        latencia_s=round(elapsed_s, 3),
        custo_usd=round(compute_cost(tokens_in, tokens_out, backend), 6),
        model_backend=backend,
        pipeline=pipeline,
    )
