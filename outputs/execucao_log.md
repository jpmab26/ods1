# Log de Execução — Co-gerador de Testes de Sistema

Log cumulativo de checkpoints (acrescente, não sobrescreva).

---

## CP0 — Bootstrap (2026-06-28)

### O que foi feito

- Criada a estrutura completa de diretórios conforme Seção 2 do plano
- Criados: CLAUDE.md, README.md, requirements.txt, .env.example, .gitignore, Makefile
- Copiado user-stories.md para data/user_stories/user-stories.md
- Criados stubs de todos os módulos Python (src/, ingestion/, eval/, tests/, prompts/)
- Criados prompts completos dos agentes A1–A4 e zero_shot (Apêndice A do plano)
- Criados schemas Pydantic conforme Apêndice B
- Copiado plano de implementação para docs/plano_implementacao_claude_code.md

### Suposições assumidas

- O diretório raiz do projeto é /home/linux/code/ufrj/ods1 (repositório git já inicializado)
- O arquivo user-stories.md existente na raiz é a fonte canônica das 21 US
- google-adk ainda não instalado neste ambiente; a instalação ocorrerá via `make bootstrap`
- O modelo de embeddings `models/text-embedding-004` é a âncora provisória (confirmar antes do CP1)
- A interface LlmAgent/SequentialAgent/LoopAgent do ADK será confirmada na documentação vigente no CP2

### Próximos passos

- ✅ Pergunta de bloqueio respondida (ver abaixo)
- ✅ `make bootstrap` executado: google-adk==2.3.0 instalado com venv
- ✅ `pytest`: 26 passed, 2 skipped (esperado)
- → Prosseguir ao CP1

---

## Resposta à pergunta de bloqueio (Seção 9) — 2026-06-28

**Credenciais disponíveis:** apenas `GOOGLE_API_KEY` (sem `ANTHROPIC_API_KEY`).

**Consequências:**
- T0-Gemini e T1 (Gemini backend): executarão com API real ✓
- T0-Claude e T2 (Claude backend): usarão `MODEL_BACKEND=dryrun`; resultados marcados como `"modo": "dry_run"` e excluídos da agregação estatística final
- T2 ficará pendente para execução real quando `ANTHROPIC_API_KEY` estiver disponível

---

## CP1 — Schemas e Ingestão/RAG (2026-06-28)

### O que foi feito

- Clonado monitoria-app (commit af39fc56) em data/repo_cache/monitoria-app
- Geradas 27 user stories individuais em data/user_stories/individual/ (parse_user_stories.py)
  - US06 → 3 sub-histórias (a/b/c); US18 → 5 sub-histórias (a/b/c/d/e)
- Gerados 1100 chunks de repositório (364 md, 15 sql, 694 py, 27 us) via chunk_repository.py
- Atualizado embed_and_index.py e retriever.py para usar google.genai SDK (substituindo google.generativeai deprecado)
  - API: client.models.embed_content(model=..., contents=..., config=EmbedContentConfig(task_type=...))
  - Resposta: result.embeddings[0].values

### Bloqueio pendente

- `make index` aguarda criação de `.env` com `GOOGLE_API_KEY` pelo usuário
- test_retriever_smoke.py está com skip até ChromaDB ser populado

---

## CP2 — Pipeline Multiagente e Runner ADK (2026-06-28)

### O que foi feito

1. **DryRunModel reescrito** como subclasse de `BaseLlm` (Pydantic BaseModel) com assinatura
   correta: `generate_content_async(self, llm_request: LlmRequest, stream=False)` retorna
   `AsyncGenerator[LlmResponse, None]` com `Content(parts=[Part(text=...)])`.

2. **exit_tools.py substituído** por re-exportação da ferramenta nativa do ADK:
   `from google.adk.tools.exit_loop_tool import exit_loop` (define escalate=True + skip_summarization=True).

3. **Risco R1 testado empiricamente** (tests/test_adk_loop_escalation.py):
   - Resultado: **Risco R1 NÃO ocorre** em google-adk 2.3.0.
   - LoopAgent absorve o sinal escalate internamente; SequentialAgent verifica apenas
     `should_pause_invocation` (long-running tools) e NÃO reage a escalate → Echo3 executou.
   - **Estratégia A mantida** (SequentialAgent + LoopAgents).

4. **Divergência R2 documentada**: tanto `LoopAgent` quanto `SequentialAgent` estão deprecated
   em ADK 2.3.0 com mensagem "Please use Workflow instead." Decisão: manter por enquanto,
   monitorar em versões futuras; watcher de deprecation está no log de warnings do pytest.

5. **Correção de parent único**: `build_pipeline()` agora instancia A1 três vezes (a1, a1b, a1c)
   para satisfazer a restrição do ADK de que cada instância de agente só pode ter um pai.

6. **Prompts corrigidos**: variáveis de template alinhadas com output_key dos agentes:
   - `{critica_a2}` → `{critica_cobertura?}`; `{relatorio_a3}` → `{relatorio_factual?}`
   - `{verificacoes_a3}` → `{relatorio_factual?}`; `{contexto_recuperado}` → `{contexto_recuperado?}` (em todos os agentes)

7. **ADK Runner integrado** em eval/runner.py:
   - InMemorySessionService + Runner com app_name="cogerador_testes"
   - Estado inicial da sessão pré-populado com `{"user_story": us_text}`
   - Extração de casos de `session.state[output_key]` pós-execução

### Resultados

- `make test`: 27 passed, 1 skipped (retriever aguarda ChromaDB)
- `make smoke-adk` (MODEL_BACKEND=dryrun, US01, 1 repetição): saída válida gerada em
  outputs/raw/t2_US01_01.json com casos_gerados, intermediarios, tokens=0, modo=dry_run

### Próximos passos

- CP1 pendente: usuário deve criar `.env` com `GOOGLE_API_KEY=<chave>` e rodar `make index`
- CP3: seleção de US e construção do oráculo (protocolo manual com equipe)
- CP4: `make run-t0 && make run-t1` com GOOGLE_API_KEY real
