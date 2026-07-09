# Co-gerador de Testes de Sistema — monitoria-app

Pipeline multiagente (Google ADK) que gera casos de teste de sistema a partir de user stories do [`monitoria-app`](https://github.com/WillianPessoa/monitoria-app), combinando RAG sobre o repositório-alvo com quatro agentes especializados e revisão humana final.

**Sistema-alvo:** Python/Flask + MySQL para gestão de monitoria acadêmica (UFRJ 2026.1).  
**Disciplina:** Desenvolvimento de Software 1 — UFRJ.

---

## Como funciona

### O problema

Dada uma user story em texto, gerar um conjunto de casos de teste de sistema que
um(a) QA experiente escreveria — cobrindo fluxo principal, alternativos, bordas e
erros — sem alucinar regras de negócio que não existem no código real do
`monitoria-app`.

### Fluxo do pipeline multiagente

```
User Story (texto)
      │
      ▼
 A1 — Gerador            ←── RAG (ChromaDB)
      │ gera casos_atuais por particionamento de equivalência
      ▼
 LoopAgent [A2 Crítico de Cobertura  →  A1b Gerador]   (até 3 iterações)
      │ A2 aponta lacunas de cenários não cobertos; A1b acrescenta casos
      │ chama exit_loop quando não há lacunas novas
      ▼
 LoopAgent [A3 Verificador Factual  →  A1c Gerador]    (até 3 iterações)
      │ A3 ancora cada caso em evidência do código-fonte (RAG); A1c corrige
      │ chama exit_loop quando tudo está SUPORTADO ou marcado NAO_VERIFICAVEL
      ▼
 A4 — Curador
      │ remove verbosidade/redundância introduzida pelo RAG, produz lista final
      ▼
 outputs/raw/<tratamento>_<US>_<rep>.md  (Markdown estruturado)
      │
      ▼
 revisão humana (eval/labeling.py) — aprovação final, caso a caso
```

Cada um dos quatro agentes ataca uma falha documentada na literatura de geração
de testes por LLM: A1 cobre o caso-base; A2 ataca a **omissão sistemática de
cenários implícitos**; A3 ataca **alucinação de regra de negócio** (Incorrect
Fact); A4 ataca a **verbosidade excessiva** que o RAG tende a introduzir.

O tratamento **T0 (zero-shot)** é o mesmo LlmAgent A1, mas sem RAG e sem os
laços de crítica/verificação — serve de linha de base para medir o ganho do
pipeline multiagente.

### RAG

**Indexação** (`make index`): o código-fonte, schema do banco e documentação do
`monitoria-app` são divididos em chunks por estrutura semântica —
`ingestion/chunk_repository.py` quebra Markdown por cabeçalho, SQL por
`CREATE TABLE`, Python por função/classe (via AST), excluindo `backend/tests/`
para não duplicar lógica já presente nos services. Cada chunk é embutido
localmente com `paraphrase-multilingual-mpnet-base-v2` (`sentence-transformers`,
768 dim, vetores normalizados, sem custo de API) e indexado num ChromaDB local
em **espaço de cosseno** (`hnsw:space="cosine"`), o que torna a distância
devolvida interpretável como similaridade — sem isso, o espaço padrão do
Chroma (L2) não tem escala utilizável para calibrar limiar de confiança.

**Recuperação** (`src/tools/retriever.py:recuperar_contexto`): busca **híbrida**
— combina busca vetorial (semântica, captura sinônimo/paráfrase) com BM25
(léxica, captura correspondência exata de identificador — ex. nome de status
como `PENDENTE_APROVACAO`, que um embedding genérico tende a não distinguir
bem). Os dois rankings são fundidos via Reciprocal Rank Fusion. Cada resultado
vem com um rótulo de confiança (`alta` / `media` / `lexical` / `baixa`)
derivado da similaridade de cosseno, e resultados puramente vetoriais abaixo
de um piso mínimo são descartados — a função pode devolver lista vazia
deliberadamente, em vez de forçar `k` resultados mesmo sem nada relevante.

A recuperação tem duas camadas:
1. **Garantida**: antes do pipeline rodar, `eval/runner.py` já busca pela
   user story inteira e popula o estado inicial `contexto_recuperado` — isso
   garante um contexto de partida independente da disciplina de tool-calling
   do modelo (importante para os backends gratuitos/menores do T2/T3).
2. **Agentic**: A1, A2 e A3 também têm a tool `recuperar_contexto` disponível
   para buscas adicionais e mais específicas durante os laços de crítica/verificação.

O tratamento T0 (zero-shot) nunca usa RAG — nem a camada garantida nem a tool —
por desenho, para servir de linha de base.

### Formato de saída

Todos os agentes produzem **Markdown estruturado** — o LLM nunca é solicitado a
gerar JSON, eliminando uma classe inteira de falhas de parsing:

```markdown
### US01-CT01 — Cadastro bem-sucedido de aluno
- **Pré-condição:** Admin autenticado; email 'novo@teste.com' não existe no banco
- **Objetivo:** Verificar criação de usuário aluno com status PENDENTE
- **Resultado esperado:** Usuário criado; senha temporária exibida; flash de sucesso
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: cria usuário com status PENDENTE — fonte: backend/usuarios/service.py#create_user (tipo: código)
- **Origem:** A1
- **Aprovado humano:** pendente
```

`src/parsers.py` converte esse Markdown em `list[dict]` deterministicamente
(sem depender do LLM para estruturar dados).

### O que é avaliado

A pergunta central: **o pipeline multiagente produz casos de teste melhores do
que pedir direto ao modelo (zero-shot)? E isso compensa usar um modelo menor?**

| Tratamento | Pipeline | Backend |
|------------|----------|---------|
| T0-GeminiFlash | zero-shot | gemini-2.5-flash |
| T0-Nvidia | zero-shot | nemotron-ultra-550b *(modelo maior, só zero-shot)* |
| T0-NvidiaSuper | zero-shot | nemotron-super-120b |
| T0-OpenAI-OSS | zero-shot | gpt-oss-120b |
| **T1** | multiagente | gemini-2.5-flash *(par direto com T0-GeminiFlash)* |
| **T2** | multiagente | nemotron-super-120b *(par direto com T0-NvidiaSuper)* |
| ~~T3~~ | ~~multiagente~~ | ~~gpt-oss-120b~~ — **ABANDONADO DEFINITIVAMENTE**: `gpt-oss-120b:free` sofre rate limiting upstream persistente no OpenRouter, retentado múltiplas vezes ao longo do projeto (inclusive com checkpoint por estágio, que ajudou a execução a avançar mais no pipeline mas não o suficiente para completar). Investigação descartou limitação de contexto do modelo (131k tokens) como causa. |

Cada Tx-pipeline tem um T0 com o **mesmo modelo** (comparação isolando o efeito
da arquitetura) e o T0 extra (Nvidia-Ultra) serve para comparar um modelo
grande em zero-shot contra um modelo pequeno com pipeline. T3 foi descartado
por indisponibilidade da API; a análise comparativa usa T0 (4 backends) + T1 + T2.

Métricas calculadas (`eval/metrics.py`, `eval/statistics.py`) sobre os casos
gerados, comparados ao oráculo manual caso a caso:

- **Precisão, Recall, F1** — correspondência semântica com o oráculo (VP/FP/FN). Rotulagem 100% humana: os 438 casos gerados foram revisados individualmente por um desenvolvedor contra o código real do `monitoria-app` (não contra a user story em prosa nem por LLM-juiz) — ver `documento_completo.md`, Seção 2.5.
- **Taxonomia de defeito** (Travassos et al., 1999) para os falsos positivos: Incorrect Fact, Ambiguity, Inconsistency, Extraneous Information
- **Verbosidade média** e **% de informação supérflua** (efeito colateral do RAG)
- **Significância estatística**: teste de Friedman entre tratamentos + pós-teste de Wilcoxon pareado com correção de Holm
- **Custo e latência** por execução (`eval/instrumentation.py`)

### Oráculo (gold standard)

`data/oracle/oraculo_consolidado.md` — 27 casos cobrindo as 4 US efetivamente
testadas: **US01** (EP01 — cadastro de usuários), **US04** (EP01 — admin
desativa usuário), **US07** (EP02 — professor indica monitor), **US08** (EP02
— aprovação de indicação de monitor). US01/US08 revisadas por ≥ 2 revisores
humanos; US04/US07 construídas em rodada posterior com "revisores" simulados
por LLM (Kappa abaixo da meta — ver `data/oracle/selecao_us_oraculo.md`).
Escala de relevância 1/3/5, Kappa ponderado linear como critério de
concordância. Todos os 27 casos passaram por revisão humana final contra o
código real do `monitoria-app` e estão `Aprovado humano: sim`. Toda evidência
ancorada em código executável, nunca em `backend/tests/` (essa pasta foi
escrita às pressas, sem revisão, e é excluída deliberadamente do RAG e do
oráculo). Protocolo completo e justificativa da seleção em
`data/oracle/selecao_us_oraculo.md`.

Nenhum código gera o oráculo automaticamente — é um artefato humano editado
diretamente em Markdown. `src/parsers.py` extrai os casos para comparação.

---

## Como usar

### Início rápido

```bash
cp .env.example .env        # preencha as chaves de API (veja abaixo)
make bootstrap               # cria .venv e instala dependências
make ingest                  # clona monitoria-app e processa user stories
make index                   # gera embeddings e popula ChromaDB
make smoke-adk                # valida o pipeline sem chamadas de API (dryrun)
make smoke-gemini-flash       # valida integração real com Gemini Flash
```

### Backends disponíveis

Selecione com `MODEL_BACKEND=<valor>` (em `.env` ou na linha de comando):

| `MODEL_BACKEND` | Modelo | Chave necessária |
|-----------------|--------|-----------------|
| `gemini_flash` | gemini-2.5-flash (free tier) | `GOOGLE_API_KEY` |
| `nvidia` | nemotron-3-ultra-550b (free tier) — **zero-shot only**, ver nota abaixo | `OPENROUTER_API_KEY` |
| `nvidia_super` | nemotron-3-super-120b (free tier) | `OPENROUTER_API_KEY` |
| `openai_oss` | gpt-oss-120b (free tier) | `OPENROUTER_API_KEY` |
| `dryrun` | fixture local, sem API | — |

Todos os backends usados no experimento rodam em tier gratuito — custo em US$ é 0,00 em todas as execuções (ver `documento_completo.md`, Seção 4.3).

`nvidia` (Nemotron Ultra 550B) só roda no tratamento T0 (zero-shot) — `eval/runner.py`
rejeita `--pipeline multiagent --backend nvidia` com erro explícito. O modelo é grande
demais para justificar o custo das até 14 chamadas extra por execução que o pipeline
multiagente pode fazer (A1 + até 3×[A2,A1b] + até 3×[A3,A1c] + A4).

### Rotação de chaves

O runner suporta até **6 chaves por provedor**, com rotação round-robin
automática a cada execução (`eval/runner.py:_rotate_api_keys`):

```env
GOOGLE_API_KEY_1=chave1
GOOGLE_API_KEY_2=chave2
GOOGLE_API_KEY_3=chave3
GOOGLE_API_KEY_4=chave4
GOOGLE_API_KEY_5=chave5
GOOGLE_API_KEY_6=chave6

OPENROUTER_API_KEY_1=chave1
OPENROUTER_API_KEY_2=chave2
OPENROUTER_API_KEY_3=chave3
OPENROUTER_API_KEY_4=chave4
OPENROUTER_API_KEY_5=chave5
OPENROUTER_API_KEY_6=chave6
```

Não é preciso preencher as 6 — índices ausentes no `.env` são simplesmente
ignorados, e a rotação ocorre apenas entre as chaves efetivamente definidas.
Fallback: se nenhuma `GOOGLE_API_KEY_N` existir, usa `GOOGLE_API_KEY` (chave
única); idem para OpenRouter.

### Comandos principais

```bash
make run-all      # executa T0×4 + T1 + T2 (T3 abandonado — ver tabela acima)
make eval         # rotulagem humana interativa + métricas + significância estatística
make consolidate  # gera tabelas e resultados_consolidados.json
make test         # pytest
make clean        # remove artefatos gerados
```

Sem terminal interativo disponível (ex.: execução automatizada), a rotulagem
pode ser feita editando diretamente `outputs/rotulagens/{execução}.labels.json`
no mesmo formato que `eval/labeling.py` produziria, seguida de:

```bash
python -m eval.metrics
python -m eval.statistics
```

O julgamento (VP/FP contra o código real do sistema-alvo) continua humano em
qualquer um dos dois caminhos — não há LLM-juiz no projeto.

---

## Estrutura do projeto

```
src/
  agents/       — A1…A4 (LlmAgent)
  tools/        — retriever.py (RAG híbrido, com metadado de rota/call-graph)
  model_backends.py — get_model(role), seletor por MODEL_BACKEND
  parsers.py    — Markdown → list[dict]
  pipeline.py   — build_pipeline (atômico) / build_pipeline_stages (com checkpoint)
  zero_shot.py  — runner zero-shot sem pipeline
ingestion/
  clone_repo.py, parse_user_stories.py — ingestão do monitoria-app
  chunk_repository.py — chunking + análise estática de call-graph (rotas Flask)
  embed_and_index.py  — ChromaDB + embeddings locais
eval/
  runner.py             — orquestrador de experimentos, rotação de chaves, checkpoint por estágio
  labeling.py           — rotulagem VP/FP/FN humana interativa
  retrieval_eval.py     — avaliação empírica de recall@k do RAG
  metrics.py            — precisão, recall, F1, verbosidade
  statistics.py         — Friedman, Wilcoxon, kappa
  consolidate.py        — artefatos finais em Markdown
  instrumentation.py    — tokens, latência, custo
prompts/        — Markdown, um arquivo por agente
data/
  oracle/       — oraculo_consolidado.md, selecao_us_oraculo.md
  user_stories/ — user stories parseadas do monitoria-app
outputs/raw/    — saídas brutas (.json + .md por execução)
tests/          — suíte pytest
```
