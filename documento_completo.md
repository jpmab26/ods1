# Co-gerador de Testes de Sistema — Documento Consolidado do Projeto

**Projeto:** `cogerador-testes-monitoria` — UFRJ, Desenvolvimento de Software 1
**Sistema-alvo:** [`monitoria-app`](https://github.com/WillianPessoa/monitoria-app) (Python/Flask + MySQL, gestão de monitoria acadêmica)
**Escopo oficial deste documento:** 4 user stories (US01, US04, US07, US08) × 2 repetições × 6 tratamentos (T0×4 backends + T1 + T2), 48 execuções, 438 casos de teste gerados no total. T3/gpt-oss-120b (pipeline) abandonado definitivamente (rate limiting persistente no OpenRouter). Todos os 438 casos gerados, mais o oráculo completo (27 casos), foram revisados individualmente por um desenvolvedor contra o código real do `monitoria-app` — não há rotulagem por LLM neste documento (Seções 2.5 e 3).

Este documento reúne, num único arquivo, tudo que é relevante para escrever o artigo final: documentação da solução, oráculo completo, métricas, relatório estatístico e discussão dos resultados. É um documento de **referência/compilação**, não o relatório final formatado (introdução, trabalhos relacionados etc. ainda precisam ser escritos em prosa acadêmica a partir daqui).

---

## 1. Visão geral da solução

### 1.1 O problema

Dada uma user story em texto, gerar um conjunto de casos de teste de sistema que um(a) QA experiente escreveria — cobrindo fluxo principal, alternativos, bordas e erros — sem alucinar regras de negócio que não existem no código real do `monitoria-app`.

### 1.2 Tese de inovação — pipeline multiagente com RAG e humano no loop

A solução não é um LLM único em prompt único: é um pipeline com **quatro agentes especializados** que se criticam mutuamente, implementado em **Google ADK**.

```
User Story (texto)
      │
      ▼
 A1 — Gerador            ←── RAG (ChromaDB, híbrido BM25+vetorial)
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
      │ deduplica, padroniza, remove verbosidade herdada do RAG, produz lista final
      ▼
 outputs/raw/<tratamento>_<US>_<rep>.md  (Markdown estruturado)
      │
      ▼
 revisão humana (eval/labeling.py) — aprovação final, caso a caso
```

Cada um dos quatro agentes ataca uma falha documentada na literatura de geração de testes por LLM: A1 cobre o caso-base; A2 ataca a **omissão sistemática de cenários implícitos** (Silva et al., 2026); A3 ataca **alucinação de regra de negócio** (*Incorrect Fact*, Travassos et al., 1999); A4 ataca a **verbosidade excessiva** que o RAG tende a introduzir (Correia et al., 2025).

O tratamento **T0 (zero-shot)** é o mesmo LlmAgent A1, mas sem RAG e sem os laços de crítica/verificação — serve de linha de base para medir o ganho do pipeline multiagente.

### 1.3 Prompts finais dos agentes (versão efetivamente usada nos experimentos)

#### A1 — Gerador (`prompts/a1_gerador.md`)

```
PERSONA: Você é um(a) Analista de QA Senior, certificado(a) ISTQB CTFL, especialista em
elaborar casos de teste de sistema a partir de user stories de software acadêmico/administrativo
em português do Brasil.

CONTEXTO DO SISTEMA: O sistema é o "monitoria-app", desenvolvido em Python/Flask + MySQL,
para gestão de monitoria acadêmica (disciplinas, monitores, agendamentos). Abaixo está um
contexto já recuperado automaticamente do repositório (código, schema do banco e documentação)
para a user story, com confiança ("alta" | "media" | "lexical" | "baixa") indicando o quanto
cada trecho é semanticamente próximo da busca — trate "baixa" como evidência fraca, não como
fato confirmado:

<contexto_rag>
{contexto_recuperado?}
</contexto_rag>

Se esse contexto não cobrir um aspecto específico que você precisa checar (ex.: uma regra de
validação, um nome de campo, um status), use a ferramenta `recuperar_contexto` com uma busca
mais direcionada antes de assumir um comportamento.

TAREFA: Gere casos de teste de sistema para a user story a seguir, usando particionamento por
equivalência para identificar variações relevantes de entrada, estado e comportamento. Baseie-se
SOMENTE na user story e no contexto recuperado — não invente regras de negócio que não estejam
documentadas; se uma regra for ambígua, gere o caso e marque "Critérios cobertos: a confirmar".

<user_story>
{user_story}
</user_story>

Se você estiver recebendo uma crítica de cobertura ou um relatório de verificação factual de uma
rodada anterior, os casos já gerados e a crítica/relatório estão abaixo:
<casos_existentes>{casos_atuais?}</casos_existentes>
<critica_cobertura>{critica_cobertura?}</critica_cobertura>
<relatorio_factual>{relatorio_factual?}</relatorio_factual>

REGRA DE ACUMULAÇÃO: se `casos_existentes` não estiver vazio, sua saída DEVE incluir todos os
casos existentes (sem modificar os que não foram criticados) e adicionar/corrigir apenas os
casos necessários para endereçar as lacunas ou verificações da rodada atual. Não descarte
casos que já estavam corretos.

EXEMPLO DE FORMATO (1 caso-modelo):
### US01-CT01 — Login com credenciais válidas
- **Pré-condição:** Usuário cadastrado e ativo
- **Objetivo:** Validar autenticação bem-sucedida
- **Resultado esperado:** Sistema autentica e redireciona ao painel do usuário
- **Tipo:** principal
- **Critérios cobertos:** AC1
- **Origem:** A1

FORMATO DE SAÍDA: responda SOMENTE em Markdown, um bloco "### <ID_US>-CT<NN> — <nome>" por caso
de teste, com os campos acima nesta ordem (Pré-condição, Objetivo, Resultado esperado, Tipo,
Critérios cobertos, Origem). Não inclua texto fora dos blocos.
```

#### A2 — Crítico de Cobertura (`prompts/a2_critico_cobertura.md`)

```
PERSONA: Você é um(a) Engenheiro(a) de Testes especializado em análise de cobertura de
requisitos, com foco em identificar lacunas que QAs experientes encontrariam, mas que estão
ausentes dos casos gerados.

TAREFA (raciocine passo a passo, mas só exponha o resultado final):
1. Releia a user story e seus critérios de aceitação explícitos.
2. Para cada critério, pergunte: "que fluxos alternativos, condições de borda (valores vazios,
   limites de tamanho/formato, duplicidade, concorrência) e condições de erro (permissão,
   dependência de outra US) um usuário real encontraria, mesmo sem estarem escritos no
   critério?" Use o contexto recuperado do repositório para fundamentar essa inferência — e,
   se suspeitar de uma regra que o contexto abaixo não cobre, chame `recuperar_contexto` com
   uma busca específica (ex.: nome do campo, da rota ou da regra) antes de apontar a lacuna.
3. Compare essa lista derivada com os casos atualmente gerados (abaixo) e liste APENAS as
   lacunas (cenários ainda não cobertos).

<user_story>{user_story}</user_story>
<contexto_rag confianca="alta|media|lexical|baixa, por trecho">{contexto_recuperado?}</contexto_rag>
<casos_atuais>{casos_atuais?}</casos_atuais>

REGRA DE PARADA: se, após a análise, você não identificar nenhuma lacuna nova em relação à
rodada anterior, chame a ferramenta exit_loop e responda apenas com o cabeçalho seguido da
observação de que nenhuma lacuna foi identificada.

FORMATO DE SAÍDA: Markdown, com um bloco por lacuna:

## Lacunas identificadas
### LC01 — <descrição curta>
- **Tipo:** alternativo | borda | erro
- **Justificativa:** <por que isso é esperado, mesmo não estando escrito na US>

Se não houver lacunas: escreva "## Lacunas identificadas" seguido de
"_Nenhuma lacuna identificada nesta rodada._". Não repita lacunas já endereçadas nos casos atuais.
```

#### A3 — Verificador Factual (`prompts/a3_verificador_factual.md`)

```
PERSONA: Você é um(a) Revisor(a) Técnico(a) responsável por auditar casos de teste contra a
implementação real do sistema, evitando que afirmações plausíveis, porém não sustentadas pelo
código, sejam aprovadas (alucinação de domínio).

TAREFA: Para cada caso de teste abaixo, busque no contexto recuperado evidência (trecho de
código, linha do schema, seção de documentação) que sustente a pré-condição e o resultado
esperado. O contexto abaixo já vem com um rótulo de confiança por trecho (alta | media |
lexical | baixa), baseado em similaridade semântica e/ou correspondência exata de termo — NÃO
trate confiança "baixa" ou "lexical" como prova suficiente, é só um indício a investigar mais,
não evidência sustentada. Para regras de negócio específicas (limites numéricos, nomes de
status, nomes de campo), chame `recuperar_contexto` você mesmo com uma busca direcionada ao
termo exato em vez de confiar só no contexto já fornecido — busca lexical exata costuma achar
identificadores que a busca semântica perde. Priorize fontes "código" e "schema" com confiança
alta/media para verificar comportamento implementado. Classifique cada caso como:
- SUPORTADO: há evidência direta com confiança alta ou media no contexto recuperado (indique o
  tipo de fonte e a confiança).
- NAO_SUPORTADO: o contexto recuperado contradiz a afirmação (ex.: campo não existe, validação
  diferente da descrita).
- NAO_VERIFICAVEL: não há evidência com confiança suficiente para confirmar nem refutar (inclui
  o caso de `recuperar_contexto` não retornar nada, ou retornar só confiança baixa/lexical).

VERIFICAÇÃO DE ROTA (obrigatória antes de aprovar SUPORTADO com evidência de tipo "código"):
cada trecho de código no contexto recuperado vem anotado com `rota: <endpoint(s) Flask que o
alcançam>` ou `rota: sem rota associada`. Antes de classificar um caso como SUPORTADO com base
nesse trecho, confirme que a rota anotada é compatível com o fluxo HTTP da user story sob
verificação (mesmo endpoint, ou endpoint do mesmo recurso/ação descrito na US). Uma função de
nome ou conteúdo parecido, mas alcançada por uma rota de outro fluxo de negócio, NÃO sustenta o
caso — mesmo com similaridade textual alta. Se a rota estiver ausente (`sem rota associada`) ou
for incompatível com a US, rebaixe para NAO_VERIFICAVEL, mesmo que o restante do trecho pareça
relevante; não classifique como SUPORTADO só por semelhança de texto.

EVIDÊNCIA DE AUSÊNCIA (regra para não confundir "sem evidência" com "evidência de que não
existe"): se a user story descreve um comportamento e nenhum chunk sustenta esse comportamento
especificamente, MAS o contexto recuperado inclui o chunk de código que implementa o fluxo
relacionado (mesma rota/recurso) sem essa lógica — ou seja, você pode ler a função inteira do
fluxo e confirmar que o comportamento descrito simplesmente não está lá — classifique como
NAO_SUPORTADO, não NAO_VERIFICAVEL. Reserve NAO_VERIFICAVEL para quando o fluxo relevante não
foi encontrado ou recuperado com confiança suficiente para essa leitura completa; use
NAO_SUPORTADO quando você já tem o código do fluxo certo na mão e ele contradiz ou simplesmente
não contém o que a US promete.

<casos_atuais>{casos_atuais?}</casos_atuais>
<contexto_rag confianca="alta|media|lexical|baixa, por trecho">{contexto_recuperado?}</contexto_rag>

Para cada caso NAO_SUPORTADO, escreva um relatório objetivo, citando a evidência encontrada,
para que o Agente Gerador corrija a afirmação na próxima rodada.

REGRA DE PARADA: se nenhum caso for classificado como NAO_SUPORTADO nesta rodada, chame a
ferramenta exit_loop.

FORMATO DE SAÍDA: Markdown:

## Verificação factual
### <ID_CASO>
- **Status:** SUPORTADO | NAO_SUPORTADO | NAO_VERIFICAVEL
- **Evidência:** <trecho ou resumo>
- **Fonte:** <caminho/arquivo ou nota> (tipo: código | documentação | schema | humano)

## Relatório para o Gerador
<apenas se houver casos NAO_SUPORTADO; em texto livre descrevendo o que deve ser corrigido>
```

**Achado empírico que motivou as duas regras acima (ver Seção 6.3):** apesar do desenho explícito para evitar alucinação, A3 pode validar como `SUPORTADO` casos cuja evidência citada vem de uma função de código **diferente** da relevante para a user story (RAG recupera o trecho errado), ou aceitar como evidência suficiente um fluxo descrito na US mas nunca implementado no código. As regras "VERIFICAÇÃO DE ROTA" e "EVIDÊNCIA DE AUSÊNCIA" acima existem para atacar isso. A Seção 6.3 mostra que a regra funciona de forma consistente com um dos dois backends usados no pipeline, mas não com o outro.

#### A4 — Curador (`prompts/a4_curador.md`)

```
PERSONA: Você é um(a) Editor(a) de Qualidade de Testes, responsável por preparar o conjunto
final de casos de teste para revisão humana, em formato ISTQB enxuto e em Markdown.

TAREFA:
1. Deduplique casos semanticamente equivalentes (mesma pré-condição + mesmo resultado esperado),
   mantendo a união dos "Critérios cobertos" e da "Origem".
2. Padronize nomes e ids no formato "<ID_US>-CT<NN> — <nome>".
3. Reduza a verbosidade: "Objetivo" e "Resultado esperado" com no máximo 25 palavras cada;
   remova qualificações redundantes herdadas do contexto recuperado, preservando o conteúdo
   técnico e o campo "Verificação" (não resuma nem remova evidências).
4. Adicione, a cada caso, a linha "- **Aprovado humano:** pendente".
5. Para cada caso, inclua o campo "Verificação" consolidando o status de A3 no formato:
   "<STATUS> — evidência: <resumo> — fonte: <caminho> (tipo: <tipo>)".
   Se A3 não verificou o caso, use "NAO_VERIFICAVEL — evidência: não verificado".

<casos_atuais>{casos_atuais?}</casos_atuais>
<verificacoes_a3>{relatorio_factual?}</verificacoes_a3>

FORMATO DE SAÍDA: Markdown, um bloco "### <ID_US>-CT<NN> — <nome>" por caso, com os campos
exatamente nesta ordem: Pré-condição, Objetivo, Resultado esperado, Tipo, Critérios cobertos,
Verificação, Origem, Aprovado humano. Não inclua texto fora dos blocos.
```

#### Zero-shot / T0 (`prompts/zero_shot.md`)

```
PERSONA: Você é um(a) Analista de QA Senior, certificado(a) ISTQB CTFL, especialista em
elaborar casos de teste de sistema a partir de user stories de software acadêmico/administrativo
em português do Brasil.

CONTEXTO DO SISTEMA: O sistema é o monitoria-app, em Python/Flask + MySQL, para gestão de
monitoria acadêmica (disciplinas, monitores, agendamentos, presenças).

TAREFA: Gere casos de teste de sistema para a user story a seguir, usando particionamento por
equivalência para identificar variações relevantes de entrada, estado e comportamento. Baseie-se
SOMENTE na user story — não invente regras de negócio que não estejam documentadas;
se uma regra for ambígua, gere o caso e marque "Critérios cobertos: a confirmar".

<user_story>
{user_story}
</user_story>

EXEMPLO DE FORMATO (1 caso-modelo):
### US01-CT01 — Login com credenciais válidas
- **Pré-condição:** Usuário cadastrado e ativo
- **Objetivo:** Validar autenticação bem-sucedida
- **Resultado esperado:** Sistema autentica e redireciona ao painel do usuário
- **Tipo:** principal
- **Critérios cobertos:** AC1

FORMATO DE SAÍDA: responda SOMENTE em Markdown, um bloco "### <ID_US>-CT<NN> — <nome>" por caso
de teste, com os campos acima nesta ordem (Pré-condição, Objetivo, Resultado esperado, Tipo,
Critérios cobertos). Não inclua texto fora dos blocos.
```

### 1.4 RAG

**Indexação:** o código-fonte, schema do banco e documentação do `monitoria-app` são divididos em chunks por estrutura semântica — Markdown por cabeçalho, SQL por `CREATE TABLE`, Python por função/classe (via AST), excluindo `backend/tests/` para não duplicar lógica já presente nos services. Cada chunk é embutido **localmente** com `paraphrase-multilingual-mpnet-base-v2` (`sentence-transformers`, 768 dim, vetores normalizados, sem custo de API) e indexado num ChromaDB local em espaço de cosseno (`hnsw:space="cosine"`).

**Recuperação híbrida:** combina busca vetorial (semântica) com BM25 (léxica, para casar identificadores exatos como `PENDENTE_APROVACAO`). Os dois rankings são fundidos via Reciprocal Rank Fusion (k=60). Cada resultado recebe rótulo de confiança (`alta`/`media`/`lexical`/`baixa`); resultados vetoriais abaixo de um piso mínimo são descartados.

Duas camadas de recuperação: **garantida** (pré-busca em Python pela US inteira, antes do pipeline rodar) e **agentic** (tool `recuperar_contexto` disponível para A1, A2, A3 fazerem buscas adicionais). T0 (zero-shot) nunca usa RAG, por desenho — serve de linha de base.

### 1.5 Backends de modelo (100% nuvem)

| `MODEL_BACKEND` | Modelo | Uso no experimento | Custo |
|---|---|---|---|
| `gemini_flash` | gemini-2.5-flash | T0 + **T1** (pipeline) | Free tier (Google AI Studio) |
| `nvidia` | nemotron-3-ultra-550b (OpenRouter) | T0 apenas (grande demais para pipeline) | Free tier |
| `nvidia_super` | nemotron-3-super-120b (OpenRouter) | T0 + **T2** (pipeline) | Free tier |
| `openai_oss` | gpt-oss-120b (OpenRouter) | T0; **T3 (pipeline) abandonado definitivamente** | Free tier |
| `dryrun` | fixture local | smoke tests | — |

**Todos os backends usados no experimento rodam em tier gratuito** — custo em US$ é 0,00 para as 48 execuções (Seção 4.3). Rotação round-robin de até 6 chaves por provedor (`GOOGLE_API_KEY_1..6`, `OPENROUTER_API_KEY_1..6`), necessária por causa das cotas diárias baixas do tier gratuito.

### 1.6 Formato de saída

Todos os agentes produzem **Markdown estruturado** — não JSON. `src/parsers.py` converte deterministicamente em `list[dict]` para cálculo de métricas.

---

## 2. Desenho experimental

### 2.1 Perguntas de pesquisa

- **RQ1:** o pipeline multiagente reduz omissão e alucinação de domínio em relação ao zero-shot, sem perda de precisão nem aumento de verbosidade?
- **RQ2:** a arquitetura multiagente compensa a capacidade bruta do modelo? (modelo pequeno + pipeline supera modelo grande + zero-shot?)

### 2.2 Tratamentos

T0 roda com 4 backends zero-shot; T1/T2 são o pipeline multiagente pareado com o backend de mesmo modelo do T0, para isolar o efeito da arquitetura — 6 tratamentos no total.

| Tratamento | Pipeline | Backend | Status |
|---|---|---|---|
| T0-GeminiFlash | zero-shot | gemini-2.5-flash | ✅ completo |
| T0-Nvidia | zero-shot | nemotron-ultra-550b | ✅ completo |
| T0-NvidiaSuper | zero-shot | nemotron-super-120b | ✅ completo |
| T0-OpenAI-OSS | zero-shot | gpt-oss-120b | ✅ completo |
| **T1** | multiagente | gemini-2.5-flash *(par com T0-GeminiFlash)* | ✅ completo |
| **T2** | multiagente | nemotron-super-120b *(par com T0-NvidiaSuper)* | ✅ completo |
| ~~T3~~ | ~~multiagente~~ | ~~gpt-oss-120b~~ | ❌ **abandonado definitivamente** |

**T3 abandonado definitivamente:** `gpt-oss-120b:free` sofre rate limiting upstream persistente no OpenRouter, mesmo com o checkpoint por estágio do pipeline (ver abaixo): a execução completa o estágio A1 e avança até `loop_cobertura`, mas `loop_cobertura` (múltiplas chamadas internas: A2+A1b, até 3 iterações) nunca termina dentro do orçamento de tentativas. Investigação descartou limitação de contexto do modelo (131k tokens, vs. 1M do Nemotron Super que funciona) como causa: os logs nunca mostram erro de contexto excedido, só rate-limit explícito, e a falha ocorre já na 1ª chamada (A1), antes de qualquer acúmulo de contexto. Conclusão: é o tier gratuito desse modelo especificamente sobrecarregado no OpenRouter, não algo corrigível do lado do projeto. `run-all` exclui T3; `run-t3` mantido para replicabilidade futura.

**Checkpoint por estágio no pipeline multiagente.** O pipeline multiagente faz até 14 turnos de agente por execução (A1 + até 3× Loop[A2,A1b] + até 3× Loop[A3,A1c] + A4, cada turno podendo somar chamadas extras de tool-calling) — mais do que a cota diária gratuita de alguns provedores (ex.: 20 requisições/dia/projeto/modelo no Gemini) comporta numa única tentativa. `src/pipeline.py::build_pipeline_stages` quebra o pipeline atômico em 4 estágios independentes, cada um rodado via `Runner` separado sobre a mesma sessão ADK — se um estágio falhar (cota esgotada, rate limit), a tentativa seguinte pula os estágios já concluídos em vez de reiniciar do zero. Checkpoint é por estágio, não por iteração de loop dentro de um estágio (limitação aceita, relevante para o caso de T3 acima).

### 2.3 User stories e escopo (4 US oficiais)

O experimento cobre 4 US, usadas como os 4 blocos do teste de Friedman (Seção 5) — repetições (`--repeticoes 2`) não aumentam o número de blocos, só US adicionais aumentam.

| ID | Título | Épico | Justificativa |
|---|---|---|---|
| US01 | Admin cadastra usuários | EP01 — Autenticação/gestão de usuários | Validação CRUD + unicidade de email |
| US08 | Admin aprova/rejeita indicação de monitor | EP02 — Gestão de monitores | Máquina de estados com bifurcação (ATIVO/REJEITADO) |
| US04 | Admin desativa um usuário | EP01 — Perfis e Autenticação | Troca de estado simples com guarda de autoproteção (`deactivate_user`/`routes.py::deactivate`), sem dependência de outros módulos — perfil de baixo risco para o RAG |
| US07 | Professor indica aluno como monitor | EP02 — Cadastro de Disciplinas e Monitores | Criação de entidade com validação cruzada de posse (`create_indicacao`, validado contra as disciplinas do professor autenticado); complementa US08, que aprova/rejeita o que US07 cria |

### 2.4 Métricas

- Precisão, Recall, F1 — contra o oráculo manual, repetido n=2 vezes por US por tratamento
- Taxonomia de defeitos (Travassos et al., 1999): Incorrect Fact, Ambiguity, Inconsistency, Extraneous Information
- Verbosidade média (palavras em objetivo+resultado_esperado) e % Extraneous
- Custo (US$) e latência (s) por execução
- Friedman entre tratamentos (blocos = US); Wilcoxon pareado com correção Holm se significativo

### 2.5 Nota metodológica — rotulagem

A rotulagem VP/FP segue o protocolo original: julgamento **humano**, um desenvolvedor familiarizado com o código do `monitoria-app` decidindo caso a caso se o teste gerado é verdadeiro-positivo ou falso-positivo (e, se FP, a categoria de defeito de Travassos et al., 1999), sempre lendo o código-fonte real — nunca a user story em prosa nem a saída de outro LLM. Isso vale uniformemente para os **438 casos gerados nas 48 execuções** e para os **27 casos do oráculo** (Seção 3): mesma pessoa, mesmo método, mesma fonte de verdade (código executável).

**Dois bugs de integridade de dados foram encontrados e corrigidos** ao processar os resultados:
1. `src/parsers.py::parse_markdown_casos` exigia exatamente um espaço depois de `"###"` para reconhecer o início de um caso; alguns modelos geram `"###US08-CT01"` sem espaço. Quando isso acontecia, o caso (ou, se fosse a primeira linha do arquivo, **o arquivo inteiro**) desaparecia silenciosamente da contagem — sem erro, sem aviso. Corrigido para tolerar zero ou mais espaços.
2. Duas execuções (`t0_nvidia_super_US04_01`, `t2_US01_02`) tinham `.md` genuinamente vazios por falha real de geração (não bug de parsing) e foram **regeneradas** com `make run-t0`/`make run-t2` antes da rotulagem — não há nenhuma execução com F1=0,0 por vazio no conjunto final.

**Resultado da rotulagem:** dos 438 casos, **320 são verdadeiro-positivos e 118 são falso-positivos** (107 `Incorrect Fact`, 11 `Ambiguity`) — ver detalhamento por tratamento na Seção 4.2. Um padrão recorrente de alucinação (fluxo de "confirmação de substituição de monitor" em US08, nunca implementado no código real) responde por boa parte dos `Incorrect Fact` — discutido em detalhe na Seção 6.3.

Os rótulos finais estão em `outputs/rotulagens/*.labels.json` (um arquivo por execução, campo `justificativa` com a evidência de código por caso). Não há segunda passada, não há Kappa inter-avaliador para a rotulagem dos casos gerados — a limitação correspondente (avaliador único) está na Seção 7.

---

## 3. Oráculo consolidado (gold standard) — 27 casos, US01 + US04 + US07 + US08

Construído manualmente por 2 revisores (revisor1 + revisor2) para US01/US08, escala de relevância 1/3/5, limiar de aprovação soma ≥ 8, Kappa ponderado linear como critério de concordância (meta ≥ 0,41). US04/US07 foram adicionadas em rodada posterior com revisores simulados por LLM em duas passadas (Kappa de construção abaixo da meta — US04=0,25, US07=0,16, ver `data/oracle/selecao_us_oraculo.md`). Todos os 27 casos, incluindo US04/US07, passaram por revisão humana final contra o código real do `monitoria-app` e estão aprovados (`Aprovado humano: sim`) — ver nota abaixo e Seção 7, item 4, sobre a diferença entre essa aprovação e o Kappa de construção original. Fonte canônica: `data/oracle/oraculo_consolidado.md`.

**Reauditoria de evidência:** os 19 casos originais de US01/US08 citavam `backend/tests/*.py` no campo `Verificação` — proibido pelo protocolo do projeto (essa pasta foi escrita às pressas, sem revisão, e não é fonte de verdade confiável). Todos os 27 casos (incluindo os 19 antigos) foram reancorados em código executável (`backend/**/*.py` não-teste, `backend/db/schema.sql`); nenhum precisou ser marcado `NAO_VERIFICAVEL`.

**Revisão humana final:** um desenvolvedor familiarizado com o código do `monitoria-app` revisou os 27 casos um a um contra o código real (não contra a user story em prosa). Dois gaps de pré-condição foram encontrados e corrigidos em `US08-CT01`/`US08-CT11` (faltava "vinculada a uma disciplina com status ATIVA" — `approve_monitoria` faz um SELECT com JOIN em `disciplinas` checando esse status antes do UPDATE; um caso que não declarasse essa pré-condição citaria evidência incompleta do fluxo real). Após as correções, todos os 27 casos foram aprovados: `Aprovado humano: sim` em `data/oracle/oraculo_consolidado.md`.

### US01 — Admin cadastra usuários com perfis (10 casos)

| ID | Nome | Tipo | Critério |
|---|---|---|---|
| US01-CT01 | Cadastro bem-sucedido de aluno | principal | Cenário 1 |
| US01-CT02 | Cadastro bem-sucedido de professor | alternativo | Cenário 1 |
| US01-CT03 | Rejeição de email duplicado | erro | Cenário 2 |
| US01-CT05 | Rejeição de cadastro sem nome | erro | Cenário 1 |
| US01-CT06 | Rejeição de papel inválido | erro | Cenário 1 |
| US01-CT11 | Cadastro de admin cria usuário com status PENDENTE | principal | Cenário 1 |
| US01-CT12 | Senha temporária exibida ao admin após criação | principal | Cenário 1 |
| US01-CT13 | Email duplicado exato rejeitado | erro | Cenário 2 |
| US01-CT14 | Cadastro sem email rejeitado como campo obrigatório | erro | Cenário 1 |
| US01-CT15 | Papel vazio rejeitado como papel inválido | borda | Cenário 1 |

Todos verificados **SUPORTADO** contra código executável (`backend/usuarios/service.py`, `backend/usuarios/repository.py`, `backend/usuarios/routes.py`) — nenhum caso cita `backend/tests/` (proibido pelo protocolo do projeto).

**Achados de código durante a construção (não incluídos no oráculo):**
- `create_user` **não valida formato de e-mail** — só checa presença, trim e duplicidade case-insensitive (`normalized_email = email.strip().lower()`); um e-mail sintaticamente inválido (sem `@`, sem domínio, com espaço interno, com múltiplos `@`) é aceito normalmente, sem nenhuma checagem de formato no código. Este foi, isoladamente, o gap de requisito mais citado (incorretamente, como se fosse validado) pelos casos gerados em toda a rodada — 11 dos 438 casos revisados (Seção 2.5) assumem essa validação e foram rotulados `Incorrect Fact` por isso.
- `create_user` **aceita nome composto só por espaços** — o check `if not nome` roda **antes** do `.strip()`; uma string só de espaços é truthy, passa no check, e é armazenada como `""` (vazio) após `nome.strip()` no `INSERT`. Não incluído no oráculo por não ser um dos 4 cenários oficiais da US, mas gerou 3 rótulos `Incorrect Fact` (casos que assumiam rejeição).

Nenhum dos dois achados acima foi corretamente identificado por nenhuma das 438 execuções — em todo caso gerado que tocou nesses dois temas, o agente assumiu (incorretamente) que a validação existia. Contraste com o achado da Seção 6.3 (US08), onde parte das execuções **corrigiu** corretamente a alegação fabricada.

### US08 — Admin aprova ou rejeita indicação de monitor (9 casos)

| ID | Nome | Tipo | Critério |
|---|---|---|---|
| US08-CT01 | Aprovação de indicação pendente muda status para ATIVO | principal | Cenário 1 |
| US08-CT02 | Rejeição com motivo muda status para REJEITADO | principal | Cenário 3 |
| US08-CT03 | Indicação aprovada sai da lista de pendentes | principal | Cenário 4 |
| US08-CT04 | Aprovação bloqueada quando aluno já é monitor ativo | erro | Cenário 2 |
| US08-CT05 | Aprovar indicação inexistente retorna erro | erro | Cenário 1 |
| US08-CT11 | Aprovação de indicação pendente — status ATIVO no banco | principal | Cenário 1 |
| US08-CT12 | Motivo de rejeição é persistido corretamente | principal | Cenário 3 |
| US08-CT13 | Indicação rejeitada também sai da fila de pendentes | alternativo | Cenário 4 |
| US08-CT14 | Tentativa de rejeitar ID inexistente retorna erro | erro | Cenário 3 |

Todos verificados **SUPORTADO** contra código executável (`backend/monitorias/service.py`, `backend/monitorias/repository.py`, `backend/monitorias/routes.py`) — nenhum caso cita `backend/tests/` (proibido pelo protocolo do projeto).

### US04 — Admin desativa um usuário (3 casos)

| ID | Nome | Tipo | Critério |
|---|---|---|---|
| US04-CT01 | Desativação bem-sucedida de usuário ativo | principal | Cenário 1 |
| US04-CT02 | Admin não pode desativar o próprio usuário | borda | Cenário 1 (regra de autoproteção, verificada em `routes.py`, não em `service.py`) |
| US04-CT03 | Desativar usuário inexistente retorna erro | erro | Cenário 1 |

Todos verificados **SUPORTADO** contra `backend/usuarios/routes.py::deactivate`, `backend/usuarios/service.py::deactivate_user`, `backend/usuarios/repository.py::deactivate_user` (evidência de código).

**Achado de código durante a construção (não incluído no oráculo):** uma segunda chamada de desativação sobre um usuário já `INATIVO` não retorna erro — `repository.deactivate_user` roda `UPDATE ... WHERE id = %s` sem checar o status atual, `rowcount` continua > 0, e a rota mostra sucesso. É uma operação idempotente silenciosa, não a rejeição que a US sugere — candidato a bug/gap de requisito, fora do escopo desta tarefa (ver `data/oracle/selecao_us_oraculo.md`).

### US07 — Professor indica aluno como monitor (5 casos)

| ID | Nome | Tipo | Critério |
|---|---|---|---|
| US07-CT01 | Indicação bem-sucedida cria vínculo pendente de aprovação | principal | Cenário 1 |
| US07-CT02 | Indicação de aluno inválido é rejeitada | erro | Cenário 2 (nota: mensagem exibida é genérica, "Aluno inválido.", diverge do texto sugerido pela US) |
| US07-CT03 | Disciplina de outro professor não aparece nas opções do formulário | principal | Cenário 3 |
| US07-CT04 | Tentativa de indicar para disciplina de outro professor via POST forjado é rejeitada | borda | Cenário 3 (defesa em profundidade) |
| US07-CT05 | Indicação com disciplina_id inexistente é rejeitada | erro | Cenário 3 (aprovado por consenso, análogo a US08-CT05) |

Todos verificados **SUPORTADO** contra `backend/monitorias/routes.py::indicar`, `backend/monitorias/repository.py::create_indicacao`, `backend/disciplinas/repository.py::list_by_professor`, `backend/usuarios/repository.py::list_active_students` (evidência de código).

**Achado de código durante a construção (não incluído no oráculo):** a validação de "aluno já possui monitoria ativa em outra disciplina" só é aplicada na **aprovação** (`monitorias/repository.py::approve_monitoria`, ver US08-CT04), não na **indicação** (`create_indicacao`) — a constraint única da tabela é `UNIQUE (disciplina_id, aluno_id)`, não `UNIQUE (aluno_id)`, então nada impede múltiplas indicações `PENDENTE_APROVACAO` simultâneas do mesmo aluno em disciplinas diferentes antes de qualquer aprovação. Um caso que esperasse bloqueio nesse momento seria `NAO_SUPORTADO`; não incluído.

*(Texto completo de pré-condição/objetivo/resultado esperado/evidência de cada caso das 4 US em `data/oracle/oraculo_consolidado.md`.)*

---

## 4. Resultados quantitativos

### 4.1 Precisão, Recall, F1 por execução (4 US × 2 repetições × 6 tratamentos = 48 execuções)

| Tratamento | US | Rep | Precisão | Recall | F1 |
|---|---|---|---:|---:|---:|
| t0_gemini_flash | US01 | 1 | 1.0000 | 0.4000 | 0.5714 |
| t0_gemini_flash | US01 | 2 | 1.0000 | 0.4000 | 0.5714 |
| t0_gemini_flash | US04 | 1 | 0.5000 | 0.3333 | 0.4000 |
| t0_gemini_flash | US04 | 2 | 0.5000 | 0.3333 | 0.4000 |
| t0_gemini_flash | US07 | 1 | 1.0000 | 0.8000 | 0.8889 |
| t0_gemini_flash | US07 | 2 | 1.0000 | 1.0000 | 1.0000 |
| t0_gemini_flash | US08 | 1 | 0.5714 | 0.4444 | 0.5000 |
| t0_gemini_flash | US08 | 2 | 0.4000 | 0.2222 | 0.2857 |
| t0_nvidia | US01 | 1 | 0.8889 | 0.8000 | 0.8421 |
| t0_nvidia | US01 | 2 | 0.8182 | 0.9000 | 0.8571 |
| t0_nvidia | US04 | 1 | 0.8333 | 1.0000 | 0.9091 |
| t0_nvidia | US04 | 2 | 0.8000 | 1.0000 | 0.8889 |
| t0_nvidia | US07 | 1 | 0.8000 | 1.0000 | 0.8889 |
| t0_nvidia | US07 | 2 | 0.6667 | 0.8000 | 0.7273 |
| t0_nvidia | US08 | 1 | 0.6364 | 0.7778 | 0.7000 |
| t0_nvidia | US08 | 2 | 0.4545 | 0.5556 | 0.5000 |
| t0_nvidia_super | US01 | 1 | 0.8750 | 0.7000 | 0.7778 |
| t0_nvidia_super | US01 | 2 | 0.5000 | 0.4000 | 0.4444 |
| t0_nvidia_super | US04 | 1 | 0.2500 | 0.3333 | 0.2857 |
| t0_nvidia_super | US04 | 2 | 0.7500 | 1.0000 | 0.8571 |
| t0_nvidia_super | US07 | 1 | 0.7500 | 0.6000 | 0.6667 |
| t0_nvidia_super | US07 | 2 | 0.8333 | 1.0000 | 0.9091 |
| t0_nvidia_super | US08 | 1 | 0.6667 | 0.6667 | 0.6667 |
| t0_nvidia_super | US08 | 2 | 0.7000 | 0.7778 | 0.7368 |
| t0_openai_oss | US01 | 1 | 0.7500 | 0.6000 | 0.6667 |
| t0_openai_oss | US01 | 2 | 0.8000 | 0.8000 | 0.8000 |
| t0_openai_oss | US04 | 1 | 0.6667 | 1.0000 | 0.8000 |
| t0_openai_oss | US04 | 2 | 0.3333 | 1.0000 | 0.5000 |
| t0_openai_oss | US07 | 1 | 0.4286 | 0.6000 | 0.5000 |
| t0_openai_oss | US07 | 2 | 0.6250 | 1.0000 | 0.7692 |
| t0_openai_oss | US08 | 1 | 0.7000 | 0.7778 | 0.7368 |
| t0_openai_oss | US08 | 2 | 0.4444 | 0.4444 | 0.4444 |
| **t1** | US01 | 1 | 0.7000 | 0.7000 | 0.7000 |
| **t1** | US01 | 2 | 0.6429 | 0.9000 | 0.7500 |
| **t1** | US04 | 1 | 0.5000 | 1.0000 | 0.6667 |
| **t1** | US04 | 2 | 0.6667 | 0.6667 | 0.6667 |
| **t1** | US07 | 1 | 0.6364 | 1.0000 | 0.7778 |
| **t1** | US07 | 2 | 0.8571 | 1.0000 | 0.9231 |
| **t1** | US08 | 1 | 0.8333 | 1.0000 | 0.9091 |
| **t1** | US08 | 2 | 0.7727 | 1.0000 | 0.8718 |
| **t2** | US01 | 1 | 0.6875 | 1.0000 | 0.8148 |
| **t2** | US01 | 2 | 0.7333 | 1.0000 | 0.8462 |
| **t2** | US04 | 1 | 0.7143 | 1.0000 | 0.8333 |
| **t2** | US04 | 2 | 0.8571 | 1.0000 | 0.9231 |
| **t2** | US07 | 1 | 0.8182 | 1.0000 | 0.9000 |
| **t2** | US07 | 2 | 1.0000 | 1.0000 | 1.0000 |
| **t2** | US08 | 1 | 1.0000 | 1.0000 | 1.0000 |
| **t2** | US08 | 2 | 0.9286 | 1.0000 | 0.9630 |

*(fonte: `outputs/tabelas/metricas_quantitativas.md`, calculado sobre a rotulagem final descrita na Seção 2.5 — os 438 casos gerados revisados individualmente por um desenvolvedor contra o código real.)*

### 4.2 F1 médio, VP/FP/FN e taxonomia de defeitos por tratamento (agregado sobre as 4 US)

| Tratamento | Backend | F1 médio | VP | FP | FN | N casos gerados | Incorrect Fact | Ambiguity |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| T0-GeminiFlash | gemini-2.5-flash | 0.5772 | 25 | 8 | 29 | 33 | 8 | 0 |
| T0-Nvidia | nemotron-ultra-550b | 0.7892 | 50 | 19 | 10 | 69 | 19 | 0 |
| T0-NvidiaSuper | nemotron-super-120b | 0.6680 | 36 | 17 | 18 | 53 | 9 | 8 |
| T0-OpenAI-OSS | gpt-oss-120b | 0.6521 | 40 | 27 | 15 | 67 | 27 | 0 |
| **T1** | gemini-2.5-flash (pipeline) | 0.7832 | 68 | 26 | 5 | 94 | 24 | 2 |
| **T2** | nemotron-super-120b (pipeline) | **0.9101** | 101 | 21 | 0 | 122 | 20 | 1 |

**T2 (pipeline + Nemotron Super) tem o melhor F1 médio do experimento** (0,9101), com FN=0 (recall perfeito agregado sobre as 4 US). A taxa de *Incorrect Fact* por caso gerado é: T0-GeminiFlash 24,2%, T0-Nvidia 27,5%, T0-NvidiaSuper 17,0%, T0-OpenAI-OSS 40,3%, T1 25,5%, T2 16,4% — T2 e T0-NvidiaSuper têm as taxas mais baixas: o pipeline reduz alucinação de forma clara quando o backend é o Nemotron Super, mas não uniformemente entre modelos (T1, com Gemini Flash, fica na mesma faixa dos zero-shot). Nenhum caso foi classificado como `Inconsistency` ou `Extraneous Information` nesta revisão — todos os FPs caíram em `Incorrect Fact` (alucinação de comportamento/feature inexistente, majoritariamente o padrão descrito na Seção 6.3) ou `Ambiguity` (resultado esperado não comprometido com uma predição verificável).

### 4.3 Custo e latência (agregado sobre as 4 US)

| Tratamento | Custo total (US$) | Latência média (s) |
|---|---:|---:|
| T0-GeminiFlash | 0,00 *(free tier)* | 11.25 |
| T0-Nvidia | 0,00 *(free tier)* | 192.18 |
| T0-NvidiaSuper | 0,00 *(free tier)* | 24.76 |
| T0-OpenAI-OSS | 0,00 *(free tier)* | 35.99 |
| **T1** | 0,00 *(free tier)* | **118.82** |
| **T2** | 0,00 *(free tier)* | **1186.50** |

**Todos os 6 tratamentos rodam em tier gratuito — custo em US$ é 0,00 em toda a tabela.** Tabela completa por execução em `outputs/tabelas/custo_latencia.md`. A única dimensão de custo operacional real é a **latência**: T2 é ordens de grandeza mais lento que seu par zero-shot (T0-NvidiaSuper, ~48×) — efeito do checkpoint por estágio (mais overhead de inicialização de Runner/sessão entre estágios) somado a RETRIEVAL_K=10 (mais contexto por chamada). T0-Nvidia também é bem mais lento que os demais zero-shot (~192s) — variação de carga do provedor gratuito, não uma característica do modelo em si.

---

## 5. Relatório estatístico

```
Teste de Friedman (4 blocos: US01, US04, US07, US08; 6 tratamentos)
Estatística: 10.8571
p-valor: 0.054287
Significativo (α=0,05): Não
```

Calculado por `eval/statistics.py` a partir de `outputs/metricas_por_tratamento.json`. Sem significância a α=0,05, não há pós-teste de Wilcoxon — mas p=0,054 fica muito próximo do limiar, refletindo que T2 se destaca claramente dos demais tratamentos (F1=0,9101, Seção 4.2). Ainda assim, com apenas 4 blocos (US), o teste tem pouco poder estatístico, e um resultado tão perto do limiar não deve ser lido como quase-confirmação, apenas como "inconclusivo, mas sensível a pequenas mudanças na amostra".

---

## 6. Discussão dos resultados

### 6.1 RQ2 — a arquitetura compensa a capacidade bruta do modelo?

Pares de mesmo modelo (zero-shot vs. pipeline):

| Par (mesmo modelo) | Zero-shot (T0) | Pipeline | Δ F1 |
|---|---:|---:|---:|
| Gemini 2.5 Flash: T0-GeminiFlash vs. **T1** | 0.5772 | **0.7832** | **+0.2060** |
| Nemotron Super 120B: T0-NvidiaSuper vs. **T2** | 0.6680 | **0.9101** | **+0.2421** |

Nos dois pares, o **pipeline multiagente supera o zero-shot de mesmo modelo** por uma margem grande — resultado que favorece a hipótese da arquitetura. **T2 (0,9101) tem o melhor F1 absoluto do experimento**, à frente de T0-Nvidia (550B zero-shot, 0,7892) e de todos os demais. T1 (0,7832) fica muito próximo de T0-Nvidia (0,7892) — não é o melhor tratamento do experimento, mas compete de perto com o zero-shot de modelo muito maior (550B), o que ainda favorece parcialmente a hipótese de RQ2 para esse par. Cautela: US04/US07 tendem a F1 alto para quase todos os tratamentos (perfil "de baixo risco" segundo `selecao_us_oraculo.md`), o que infla o F1 médio de todo mundo.

### 6.2 RQ1 — o pipeline reduz omissão e alucinação, sem perda de precisão nem aumento de verbosidade?

**Omissão (FN):** T2 (FN=0, recall perfeito agregado) e T1 (FN=5) têm cobertura muito melhor que qualquer T0 (FN entre 10 e 29). O pipeline mantém a promessa de reduzir omissão de forma clara e consistente nos dois pares.

**Precisão/alucinação — resultado honesto, e mais cauteloso do que o de omissão:** a taxa de `Incorrect Fact` por caso gerado é T0-GeminiFlash 24,2%, T0-Nvidia 27,5%, T0-NvidiaSuper 17,0%, T0-OpenAI-OSS 40,3%, T1 25,5%, T2 16,4%. Comparando cada pipeline com seu próprio par zero-shot: T2 (16,4%) fica só marginalmente abaixo de T0-NvidiaSuper (17,0%) — praticamente empatado, não uma redução clara — e T1 (25,5%) fica ligeiramente **acima** de T0-GeminiFlash (24,2%). Ou seja, **nenhum dos dois pipelines reduz de forma clara a taxa de alucinação por caso gerado em relação ao seu zero-shot pareado**; o ganho de F1 de ambos (Seção 6.1) vem quase inteiramente da redução de omissão, não de uma melhora de precisão/alucinação. Isso é consistente com o achado qualitativo da Seção 6.3, onde a checagem de A3 contra o comportamento real do código evita o padrão de alucinação mais recorrente apenas em T2, não em T1.

**Verbosidade:** T1 (24,01 palavras/caso, 15,66% extraneous) e T2 (33,03, 13,86%) ficam dentro da faixa dos T0 (3,33%-7,18% extraneous nos backends OpenRouter, até 22-37 palavras/caso) — o Curador (A4) contém a verbosidade herdada do RAG, mas não reduz o percentual de informação supérflua abaixo do que já ocorre em boa parte dos zero-shot.

**Síntese honesta:** o pipeline multiagente entrega um ganho real e consistente de F1 e de omissão nos dois pares testados — essa parte de RQ1 se sustenta. A parte sobre alucinação não se sustenta da mesma forma: com todos os 438 casos revisados individualmente contra o código real (não apenas uma amostra de discordâncias), a taxa de `Incorrect Fact` de cada pipeline fica no mesmo patamar (ou pior) que a de seu zero-shot pareado. O ganho de qualidade do pipeline, neste experimento, é majoritariamente um ganho de cobertura (recall), não de precisão.

### 6.3 Achado qualitativo central — alucinação de fluxo inexistente em US08

Um padrão recorrente nos agentes: eles inventam um fluxo de "confirmação de substituição de monitor" para US08 — descrito de forma aspiracional no Cenário 2 da user story, mas **nunca implementado** no código real (`monitorias/repository.py::approve_monitoria` só verifica se a indicação está pendente com disciplina ativa e se o aluno já não é monitor ativo em outra disciplina — `ALUNO_JA_MONITOR` — sem nenhuma etapa de confirmação nem lógica de desativar um "monitor antigo"). O prompt de A3 inclui regras explícitas para classificar `NAO_SUPORTADO` quando o fluxo de código lido não contém a lógica descrita. Na revisão de todos os casos de US08 contra o código (Seção 2.5), esse padrão apareceu em **todos os 6 tratamentos exceto T2**:

- **T2 (pipeline + Nemotron Super):** em toda ocorrência revisada, o caso ou evita a alegação de confirmação/substituição, ou — nas execuções mais recentes do pipeline — descreve corretamente, com evidência de código, que "não existe nenhum ponto de confirmação na rota `/aprovar`" e que aprovar dois alunos diferentes para a mesma disciplina resultaria em dois monitores ativos simultâneos. É o único tratamento em que a checagem de A3 evita esse padrão de forma consistente nas duas repetições.
- **Todos os demais tratamentos (T0×4 e T1):** repetem a alegação fabricada — confirmação de substituição, "monitor antigo desativado/perde acesso" — em praticamente toda execução que testa o cenário de "disciplina já tem monitor", citando como evidência a user story em prosa (Cenário 2) em vez do código real.

**Conclusão honesta:** a regra de A3 para esse padrão específico só funciona de forma confiável com o backend Nemotron Super (usado em T2); com Gemini Flash (T1) e em zero-shot (sem A3, por definição), o padrão se repete. Isso não é uma propriedade do prompt isolada do modelo — o mesmo prompt de A3 roda em T1 e T2, e só é seguido consistentemente em um dos dois.

**Nota metodológica — alucinação do co-gerador vs. bug real do `monitoria-app`:** o `monitoria-app` tem gaps de validação reais e documentados (Seção 3): `create_user` não valida formato de e-mail nem rejeita nome só-com-espaços; `deactivate_user` reprocessa silenciosamente um usuário já inativo em vez de retornar erro; e a regra "aluno já é monitor" só é checada na aprovação, nunca na indicação. Esses quatro gaps são propriedades reais do sistema-alvo, não defeitos do co-gerador — mas a forma como cada execução **descreve** esses pontos é que determina se o caso é VP ou FP. Nos 438 casos revisados, essa distinção se comportou de forma bem desigual entre os quatro gaps:
- **E-mail sem validação de formato e nome só-com-espaços:** nenhuma das 438 execuções descreveu corretamente esses dois gaps — todo caso que tocou nesses temas assumiu (incorretamente) que a validação existia, gerando 14 rótulos `Incorrect Fact` (11 + 3, Seção 3). Aqui a alucinação é total: o co-generator nunca verificou este ponto contra o código real em nenhum backend/tratamento.
- **"Aluno já é monitor" só na aprovação / ausência de lógica de substituição em US08:** ao contrário, 6 execuções (concentradas em T2) descreveram corretamente esse comportamento com evidência de código, e foram rotuladas VP — exatamente o padrão qualitativo desta seção.

A lição para o relatório: a verificação factual (A3) funciona de forma **desigual entre temas**, não só entre backends — reduzir alucinação em um padrão específico (substituição de monitor, só com Nemotron Super) não significa que o pipeline generaliza automaticamente para outros gaps do sistema-alvo (validação de e-mail, nome). Nenhum dos 6 tratamentos verificou espontaneamente os gaps de `usuarios/service.py` contra o código antes de assumir que a validação existia.

### 6.4 Latência

Como todos os backends usados rodam em tier gratuito (Seção 1.5), **não há dimensão de custo em US$ a comparar** — a única dimensão de custo operacional real é a **latência**. T2 leva em média ~1187s por execução, ~48× mais que seu par zero-shot T0-NvidiaSuper (~25s) — efeito do checkpoint por estágio (múltiplas inicializações de Runner/sessão entre estágios) somado a RETRIEVAL_K=10. T1 leva em média ~119s, também bem acima de T0-GeminiFlash (~11s). O ganho de F1/omissão do pipeline (Seção 6.2) precisa ser julgado contra esse custo de latência — a resiliência do checkpoint por estágio (Seção 2.2) tem um preço real em tempo de execução, ainda que nenhum custo monetário adicional.

---

## 7. Limitações

1. **Avaliador único na rotulagem dos 438 casos gerados** — um só desenvolvedor revisou todos os casos contra o código real (Seção 2.5), sem uma segunda rotulagem humana independente e sem Kappa inter-avaliador para essa parte. Isso elimina o risco de viés sistemático compartilhado entre duas passadas de LLM (não há mais LLM na rotulagem), mas não elimina o risco de erro ou viés de um único revisor humano — o ideal para a versão final seria uma segunda rotulagem humana independente, mesmo que só para uma amostra.
2. **n=4 US** (US01, US04, US07, US08), 6 tratamentos — Friedman não significativo (p=0,054, Seção 5), embora próximo do limiar de 0,05. Com apenas 4 blocos, o teste tem pouco poder estatístico para conclusões fortes; um resultado tão perto da fronteira é sensível a pequenas mudanças na amostra.
3. **T3 abandonado definitivamente** — `gpt-oss-120b:free` sofre rate limiting persistente no OpenRouter mesmo com o checkpoint por estágio (que ajudou a avançar mais no pipeline, mas não o suficiente), não resolvido pelo lado do projeto. Nenhuma comparação inclui esse backend em pipeline.
4. **Oráculo de 27 casos — 8 deles (US04/US07) com Kappa de construção abaixo da meta** entre os 2 revisores simulados por LLM (0,25 e 0,16 — ver `selecao_us_oraculo.md`), mesmo após revisão humana final ter aprovado todos os 27 casos contra o código real (Seção 3). A revisão humana final valida a correção factual de cada caso individualmente; não substitui o processo de dupla-revisão independente com Kappa que a metodologia original previa para a construção do oráculo.
5. **T0-Nvidia com latência atipicamente alta** (~192s médios) — não investigado a fundo; possível variação de carga do provedor gratuito no momento da execução, não uma mudança de código.
6. **Checkpoint por estágio aumenta a latência do pipeline** — T2 leva em média ~1187s por execução, provavelmente pelo overhead de múltiplas inicializações de Runner/sessão entre estágios. Trade-off aceito em favor de resiliência a falhas de cota/rate-limit (Seção 2.2), mas não quantificado isoladamente do efeito de RETRIEVAL_K=10.
7. **Um artefato cosmético de formatação em `t2_US01_02.md`** (execução regenerada): o campo `Verificação` usa a palavra `VERIFICADO` em vez do vocabulário esperado (`SUPORTADO`/`NAO_SUPORTADO`/`NAO_VERIFICAVEL`), e o campo `Aprovado humano` vem duplicado (`- **- **Aprovado humano:** pendente**`). Confirmado que `src/parsers.py::parse_markdown_casos` extrai corretamente todos os 30 casos e todos os campos usados em métricas (id, tipo, critérios, objetivo, resultado esperado); os dois campos afetados são apenas informativos e não são consumidos por `eval/metrics.py`/`eval/instrumentation.py`. Não corrigido (não afeta os números), mas indica que os prompts de A3/A4 podem precisar de reforço adicional de formato em rodadas futuras.

---

## 8. Artefatos de suporte (fonte de dados deste documento)

- `data/oracle/oraculo_consolidado.md` — oráculo canônico (27 casos, US01+US04+US07+US08), todos com `Aprovado humano: sim`
- `data/oracle/selecao_us_oraculo.md` — justificativa da seleção e Kappa de construção do oráculo
- `outputs/metricas_por_tratamento.json` — F1 por (tratamento, US)
- `outputs/tabelas/metricas_quantitativas.md` — P/R/F1 por execução (48 execuções)
- `outputs/tabelas/custo_latencia.md` — tokens/latência/custo por execução (custo sempre 0,00, free tier)
- `outputs/retrieval_eval_sweep.json` — sweep de RETRIEVAL_K/limiares de confiança
- `outputs/resultados_consolidados.json` — consolidado programático (métricas + custo/latência por execução)
- `outputs/rotulagens/*.labels.json` — rótulos finais VP/FP/categoria de todos os 438 casos gerados, com justificativa de código por caso (48 arquivos, 4 US, 6 tratamentos)
- `prompts/*.md` — prompts finais dos 4 agentes + zero-shot (reproduzidos na íntegra na Seção 1.3)
- `eval/retrieval_eval.py` — script de avaliação de retrieval
- `eval/statistics.py` — Friedman/Wilcoxon/Kappa ponderado (usado para o teste de significância da Seção 5 e para o Kappa de construção do oráculo)
- `src/pipeline.py::build_pipeline_stages` — pipeline multiagente em estágios com checkpoint
