.PHONY: bootstrap ingest index smoke-adk smoke-gemini smoke-gemini-flash \
        smoke-nvidia smoke-nvidia-super smoke-openai-oss oracle \
        run-t0 run-t1 run-t2 run-t3 run-all eval consolidate test clean

PYTHON ?= PYTHONPATH=$(CURDIR) .venv/bin/python
PIP    ?= .venv/bin/pip

# ---------------------------------------------------------------------------
# Infraestrutura
# ---------------------------------------------------------------------------

bootstrap:
	python3 -m venv .venv
	$(PIP) install --upgrade pip --quiet
	$(PIP) install -r requirements.txt

ingest:
	$(PYTHON) ingestion/clone_repo.py
	$(PYTHON) ingestion/parse_user_stories.py

index:
	$(PYTHON) ingestion/embed_and_index.py

# ---------------------------------------------------------------------------
# Smoke tests — verificar integração antes do run completo
#
# smoke-adk          : arquitetura apenas (dryrun, sem chamadas de API)
# smoke-gemini       : 1 US real com Gemini 2.5 Flash-Lite  — economiza créditos
# smoke-gemini-flash : 1 US real com Gemini 2.5 Flash        — modelo T0 grande
# smoke-nvidia       : 1 US real com NVIDIA Nemotron Ultra    — free tier OpenRouter
# smoke-nvidia-super : 1 US real com NVIDIA Nemotron Super    — free tier OpenRouter
# smoke-openai-oss   : 1 US real com OpenAI gpt-oss-120b      — free tier OpenRouter
# ---------------------------------------------------------------------------

smoke-adk:
	MODEL_BACKEND=dryrun $(PYTHON) -m eval.runner \
	  --pipeline multiagent --backend dryrun --us US01 --repeticoes 1

smoke-gemini:
	$(PYTHON) -m eval.runner \
	  --pipeline zero_shot --backend gemini --us US01 --repeticoes 1

smoke-gemini-flash:
	$(PYTHON) -m eval.runner \
	  --pipeline zero_shot --backend gemini_flash --us US01 --repeticoes 1

smoke-nvidia:
	$(PYTHON) -m eval.runner \
	  --pipeline zero_shot --backend nvidia --us US01 --repeticoes 1

smoke-nvidia-super:
	$(PYTHON) -m eval.runner \
	  --pipeline zero_shot --backend nvidia_super --us US01 --repeticoes 1

smoke-openai-oss:
	$(PYTHON) -m eval.runner \
	  --pipeline zero_shot --backend openai_oss --us US01 --repeticoes 1

# ---------------------------------------------------------------------------
# Oráculo manual
#
# O oráculo é construído e editado diretamente em:
#   data/oracle/oraculo_consolidado.md   ← arquivo canônico (Markdown)
#   data/oracle/selecao_us_oraculo.md    ← justificativa da seleção + protocolo
#
# Nenhum código gera o oráculo automaticamente — é um artefato humano.
# O parser `src/parsers.py` extrai os casos para cálculo de métricas.
# ---------------------------------------------------------------------------

oracle:
	@echo ""
	@echo "Oráculo: data/oracle/oraculo_consolidado.md (arquivo canônico)"
	@echo "Edite esse arquivo diretamente para adicionar/corrigir casos."
	@echo "Seleção das US e protocolo: data/oracle/selecao_us_oraculo.md"
	@echo ""

# ---------------------------------------------------------------------------
# Tratamentos experimentais (CP4 — 2 US × 2 reps)
#
# T0-*  : zero-shot com 5 backends (linha de base + modelos grandes para comparação cruzada)
#   t0_gemini        → Gemini 2.5 Flash-Lite  (modelo de pipeline, para par com T1)
#   t0_gemini_flash  → Gemini 2.5 Flash        (modelo grande, zero-shot only)
#   t0_nvidia        → Nemotron Ultra 550B      (modelo grande, zero-shot only)
#   t0_nvidia_super  → Nemotron Super 120B      (modelo de pipeline, para par com T2)
#   t0_openai_oss    → gpt-oss-120b             (modelo de pipeline, para par com T3)
#
# T1    : pipeline multiagente + Gemini 2.5 Flash
# T2    : pipeline multiagente + NVIDIA Nemotron Super (120B)
# T3    : ABANDONADO — gpt-oss-120b:free sofreu rate limiting upstream persistente
#         no OpenRouter durante toda a janela de execução (múltiplas chaves, múltiplos
#         dias, 5 tentativas × 65 s cada). run-t3 é mantido para replicabilidade futura,
#         mas não faz parte do experimento final (run-all o omite).
#
# Nemotron Ultra (nvidia) roda SOMENTE zero-shot — é grande demais (550B) para
# justificar o custo de chamadas extra do pipeline multiagente (A1+A2+A1b+A3+A1c+A4
# por execução); por isso não tem alvo "run-tX" multiagente.
# ---------------------------------------------------------------------------

run-t0:
	$(PYTHON) -m eval.runner --pipeline zero_shot --backend gemini       --us all --repeticoes 2
	$(PYTHON) -m eval.runner --pipeline zero_shot --backend gemini_flash --us all --repeticoes 2
	$(PYTHON) -m eval.runner --pipeline zero_shot --backend nvidia       --us all --repeticoes 2
	$(PYTHON) -m eval.runner --pipeline zero_shot --backend nvidia_super --us all --repeticoes 2
	$(PYTHON) -m eval.runner --pipeline zero_shot --backend openai_oss   --us all --repeticoes 2

run-t1:
	$(PYTHON) -m eval.runner --pipeline multiagent --backend gemini_flash --us all --repeticoes 2

run-t2:
	$(PYTHON) -m eval.runner --pipeline multiagent --backend nvidia_super --us all --repeticoes 2

run-t3:
	$(PYTHON) -m eval.runner --pipeline multiagent --backend openai_oss   --us all --repeticoes 2

run-all: run-t0 run-t1 run-t2
# T3 (openai_oss) foi abandonado por indisponibilidade do modelo; use run-t3 se quiser retentar.

# ---------------------------------------------------------------------------
# Avaliação e artefatos
# ---------------------------------------------------------------------------

eval:
	$(PYTHON) -m eval.labeling
	$(PYTHON) -m eval.metrics
	$(PYTHON) -m eval.statistics

consolidate:
	$(PYTHON) -m eval.consolidate

test:
	$(PYTHON) -m pytest tests/ -v

clean:
	rm -rf data/repo_cache/ data/chroma/ \
	       outputs/raw/* outputs/intermediarios/* outputs/tabelas/* \
	       outputs/exemplos/* outputs/exportacoes_selenium/* \
	       outputs/metricas_por_tratamento.json outputs/relatorio_estatistico.json \
	       outputs/resultados_consolidados.json \
	       __pycache__/ .pytest_cache/
	@echo "Nota: outputs/rotulagens/ NÃO foi apagado (trabalho humano irreversível)"
