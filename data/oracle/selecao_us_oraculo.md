# Seleção das User Stories para o Experimento

## User stories testadas (N=2)

| ID | Título | Épico | Justificativa |
|----|--------|-------|---------------|
| US01 | Admin cadastra usuários | EP01 — Autenticação/gestão de usuários | Validação CRUD + unicidade de email |
| US08 | Admin aprova/rejeita indicação de monitor | EP02 — Gestão de monitores | Máquina de estados com bifurcação (ATIVO/REJEITADO) |

## Critério de seleção

Cobertura de dois épicos centrais do sistema (EP01–EP02), maximizando diversidade
de tipos de regra de negócio (CRUD + unicidade, máquina de estados com bifurcação),
dentro do orçamento de chamadas de API disponível para `make run-all`
(2 US × 2 repetições × 7 tratamentos executados: T0×5 backends + T1 + T2).

## User stories adicionadas ao oráculo nesta rodada (fora do experimento estatístico)

| ID | Título | Épico | Justificativa |
|----|--------|-------|---------------|
| US04 | Admin desativa um usuário | EP01 — Perfis e Autenticação | Mapeamento 1:1 entre título da US, rota Flask (`/desativar`, `/reativar`) e função de serviço (`deactivate_user`/`reactivate_user`); sem dependência de e-mail/notificação; sem múltiplos módulos cruzados; sem histórico de descrever comportamento ausente do código — perfil de baixo risco para o RAG e para geração de evidência confiável. Inclui regra de borda relevante (admin não pode desativar o próprio usuário), verificada em `routes.py`, não em `service.py`. |
| US07 | Professor indica aluno como monitor | EP02 — Cadastro de Disciplinas e Monitores | Mapeia para `create_indicacao` em `monitorias/service.py`, com validação de posse da disciplina e do papel do aluno feita em `monitorias/routes.py::indicar()`; complementa US08 já presente no oráculo (US07 cria a indicação que US08 aprova ou rejeita). Mesmo perfil de baixo risco de US04 (sem cruzamento de módulos além de `disciplinas/`, sem notificação). |

Estas duas US **não fazem parte do subconjunto testado em `make run-all`** (que
permanece US01+US08, por orçamento de chamadas de API já gasto no experimento
reportado). Foram adicionadas para ampliar a cobertura do oráculo como gold
standard de referência geral do projeto, e ficam disponíveis para uma rodada
futura de experimento caso o orçamento permita.

## Protocolo de construção do oráculo (casos gold standard)

1. Dois revisores independentes elaboram casos manualmente para cada US
2. Classificação na escala 1/3/5 por ambos (1=irrelevante, 5=cobre diretamente um critério de aceitação)
3. Kappa ponderado linear entre revisores (meta: ≥0,41)
4. Casos com soma 8 ou 10 entram automaticamente no oráculo; soma 6 → consenso entre revisores
5. Cada caso aprovado é ancorado em evidência do código-fonte do `monitoria-app` (campo `Verificação`)

O oráculo final está em `data/oracle/oraculo_consolidado.md` — contém 27 casos
aprovados cobrindo US01, US04, US07 e US08 (19 dos quais são o subconjunto
efetivamente comparado contra as saídas do pipeline em US01/US08).

## Reauditoria de evidência (rodada atual)

Os 19 casos de US01/US08 citavam `backend/tests/*.py` no campo `Verificação`. O
protocolo do projeto proíbe usar essa pasta como fonte de verdade (escrita às
pressas na última sprint do `monitoria-app`, sem revisão cuidadosa — usá-la
contaminaria o gold standard com os mesmos erros que o oráculo existe para
detectar). Todos os 19 casos foram reancorados em código executável
(`backend/**/*.py`, excluindo `tests/`) com sucesso — nenhum precisou ser
marcado `NAO_VERIFICAVEL`. O conteúdo de cada caso (Pré-condição/Objetivo/
Resultado esperado/Tipo/Critérios cobertos) foi mantido; apenas o campo
`Verificação` mudou. Como a evidência mudou, `Aprovado humano` foi revertido
para `pendente` em todos os 27 casos do oráculo, aguardando nova revisão humana.

## Limitação declarada: revisores simulados por LLM (US04/US07)

O protocolo original (US01/US08) previa 2 revisores humanos independentes. Para
US04 e US07 nesta rodada, os dois "revisores" ("revisor A" e "revisor B") foram
simulados por uma única instância de LLM em duas passadas com ângulos de análise
diferentes (revisor A partiu dos cenários BDD da US e buscou o código que os
sustenta; revisor B partiu do código e verificou quais cenários ele cobre,
sem reler o resultado do revisor A). **Não existe independência real entre as
duas passadas** — ambas vêm da mesma sessão/modelo, o que tende a inflar a
concordância em relação a revisores humanos genuinamente independentes, mas
paradoxalmente os valores de Kappa obtidos abaixo ficaram baixos mesmo assim
(ver tabela), o que é mais um sinal de instabilidade dos casos do que de rigor
avaliativo equivalente ao de revisores humanos. **Os valores de Kappa abaixo
não devem ser interpretados como equivalentes aos de revisores humanos reais.**
Trate o oráculo de US04/US07 como um rascunho de alta qualidade que precisa de
aprovação humana antes de virar gold standard definitivo — o mesmo tratamento já
dado à rotulagem VP/FP (Seção 2.5 do documento consolidado do projeto).

## Kappa ponderado por US (esta rodada)

| US | Kappa ponderado linear | Interpretação (Landis & Koch) | N candidatos avaliados | Recalculado nesta rodada? |
|----|------------------------|-------------------------------|-------------------------|---------------------------|
| US01 | não disponível | — | — | Não — Tarefa 2 alterou apenas o campo `Verificação`; as notas de relevância 1/3/5 e a seleção de casos da rodada original não foram reavaliadas. O protocolo original (`selecao_us_oraculo.md` anterior) não registrava o valor numérico do Kappa obtido, apenas a meta (≥0,41). |
| US08 | não disponível | — | — | Idem US01. |
| US04 | 0,25 | Razoável | 6 | Sim — calculado com `eval/statistics.py::weighted_kappa_linear` sobre as notas de revisor A/B sobre 6 casos candidatos (3 aprovados, 1 excluído por consenso, 1 excluído por baixa relevância, 1 aprovado por relevância mas depois marcado NAO_SUPORTADO na etapa de evidência — ver achados abaixo). |
| US07 | 0,16 | Leve | 7 | Sim — calculado sobre 7 casos candidatos (5 aprovados, 1 excluído por consenso, 1 aprovado por relevância mas depois marcado NAO_SUPORTADO). |

Os valores de US04 (0,25) e US07 (0,16) ficam abaixo da meta de ≥0,41 herdada do
protocolo original. Isso é esperado dado o método de simulação de dois
revisores por uma única instância de LLM (ver limitação acima) e reforça a
necessidade de revisão humana antes de qualquer uso desses 8 casos novos como
gold standard definitivo.

## Cenários descritos na US sem implementação correspondente (achados desta rodada)

Achados de código encontrados ao tentar ancorar evidência para casos com nota
de relevância alta (candidatos que, pela escala 1/3/5, pareciam claramente
relevantes), mas para os quais o código do `monitoria-app` não implementa o
comportamento prometido pela US. Em ambos os casos, o caso candidato foi
excluído do oráculo (marcado `NAO_SUPORTADO`) em vez de ter uma evidência
inventada — são achados relevantes por si só, não falhas do processo:

1. **US04, Cenário 2 ("Usuário já desativado" deve retornar erro):** o código
   de `usuarios/repository.py::deactivate_user` executa
   `UPDATE usuarios SET status = 'INATIVO' WHERE id = %s` sem checar o status
   atual — uma segunda chamada de desativação sobre um usuário já INATIVO
   ainda casa com o `WHERE id = %s`, `rowcount` continua > 0, e a função
   retorna `True` normalmente. `routes.py::deactivate` então exibe
   `flash("Usuário desativado com sucesso.", "success")` na segunda tentativa
   — **não há erro algum**, ao contrário do que a US promete. É uma operação
   idempotente silenciosa, não uma rejeição. Caso não incluído no oráculo;
   fica como candidato a bug/gap de requisito para reporte à equipe do
   `monitoria-app` (fora do escopo desta tarefa, que só corrige o oráculo).

2. **US07 (achado de código, não descrito explicitamente como cenário na US,
   mas com nota de relevância alta por ambos os revisores simulados):** a
   validação de que "o aluno já possui monitoria ativa em outra disciplina"
   (`ALUNO_JA_MONITOR`, ver `US08-CT04`) só é aplicada em
   `monitorias/repository.py::approve_monitoria` — no momento da **aprovação**,
   não no momento da **indicação** (`create_indicacao`/`routes.py::indicar`).
   A chave única da tabela `monitorias` é `UNIQUE (disciplina_id, aluno_id)`
   (ver `db/schema.sql`), não `UNIQUE (aluno_id)` — logo nada impede que o
   mesmo aluno acumule múltiplas indicações `PENDENTE_APROVACAO` em
   disciplinas diferentes simultaneamente antes de qualquer aprovação. Um
   caso de teste que esperasse bloqueio nesse momento seria `NAO_SUPORTADO`.
   Não incluído no oráculo.

## Casos excluídos por consenso (soma de notas = 6, decisão registrada)

- **US04 — "Desativar usuário com status PENDENTE (ainda não ativo)":** notas
  3/3. Decisão de consenso: **excluir**. A US04 e seu Cenário 1 se referem
  explicitamente a "usuário ativo"; testar a desativação de um usuário
  PENDENTE reutilizaria o mesmo caminho de código de US04-CT01 sem agregar
  sinal novo relevante ao critério de aceitação escrito.
- **US07 — "Reenvio de indicação após rejeição anterior volta para pendente de
  aprovação":** notas 3/3. Decisão de consenso: **excluir**. É um
  comportamento real de `create_indicacao` (`ON DUPLICATE KEY UPDATE ... IF
  (status = 'REJEITADO', 'PENDENTE_APROVACAO', status)`), mas não corresponde
  a nenhum critério de aceitação explícito de US07 — pertence mais a uma
  eventual US futura sobre reenvio de indicação. Registrado aqui para não se
  perder, mas fora do oráculo desta rodada para evitar scope creep.
- **US07 — "Indicação com disciplina_id inexistente é rejeitada":** notas 3/3.
  Decisão de consenso: **incluir** (US07-CT05). Justificativa: é análogo a
  casos de borda já valorizados no oráculo existente (ex.: `US08-CT05`,
  "aprovar indicação inexistente"), reforça a cobertura de entradas inválidas
  no mesmo fluxo do Cenário 3, e tem evidência de código direta e barata de
  verificar (mesma checagem de `US07-CT04`).

## Caso excluído por baixa relevância (soma de notas ≤ 4)

- **US04 — "Reativação de usuário desativado":** notas 1/3. O código de
  `reactivate_user`/`/reativar` existe e foi mapeado na Tarefa 1, mas **não há
  nenhuma User Story no backlog** (nem US04, nem outra dentre as 9 do
  diretório `data/user_stories/individual/`) que descreva reativação de
  usuário — nem sequer US05, que cobre reset de senha, mas não reativação.
  Como não há critério de aceitação de nenhuma US ao qual ancorar a
  relevância do caso, ele fica fora do oráculo por ora. Registrado aqui como
  observação (possível lacuna de rastreabilidade requisito↔código, não um bug
  de comportamento) para decisão futura da equipe sobre criar uma US
  dedicada.
