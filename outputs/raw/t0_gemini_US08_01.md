### US08-CT01 — Aprovação de indicação de monitor para disciplina sem monitor ativo
- **Pré-condição:** Admin está logado. Existe uma indicação de monitor para uma disciplina que não possui nenhum monitor ativo cadastrado, com status "Pendente de aprovação".
- **Objetivo:** Validar a aprovação de uma nova indicação de monitor para uma disciplina que ainda não tem monitor.
- **Resultado esperado:** O vínculo do monitor com a disciplina muda para o status "Ativo". O aluno associado à indicação ganha permissões de monitor para a disciplina. A indicação não aparece mais na lista de pendências.
- **Tipo:** principal
- **Critérios cobertos:** AC1, AC4

### US08-CT02 — Aprovação de alteração de monitor para disciplina com monitor ativo
- **Pré-condição:** Admin está logado. Existe uma indicação de alteração de monitor para uma disciplina que já possui um monitor ativo cadastrado. A indicação está com status "Pendente de aprovação de alteração de monitor".
- **Objetivo:** Validar a aprovação da troca de um monitor por outro em uma disciplina que já possui um monitor ativo.
- **Resultado esperado:** O sistema apresenta uma mensagem de confirmação para a alteração do monitor antigo pelo novo. Ao confirmar, o vínculo do novo monitor com a disciplina muda para o status "Ativo". Apenas o novo aluno ganha permissões de monitor para a disciplina. O monitor antigo perde suas permissões. A indicação não aparece mais na lista de pendências.
- **Tipo:** principal
- **Critérios cobertos:** AC2, AC4

### US08-CT03 — Rejeição de indicação de monitor com registro de motivo
- **Pré-condição:** Admin está logado. Existe uma indicação de monitor com status "Pendente de aprovação".
- **Objetivo:** Validar a rejeição de uma indicação de monitor, com o registro do motivo da rejeição.
- **Resultado esperado:** O vínculo do monitor com a disciplina muda para o status "Rejeitado". O motivo informado pelo admin é registrado no sistema associado à indicação. A indicação não aparece mais na lista de pendências.
- **Tipo:** principal
- **Critérios cobertos:** AC3, AC4

### US08-CT04 — Visualização da lista de indicações pendentes após processamento
- **Pré-condição:** Admin está logado. Existem múltiplas indicações de monitor com status "Pendente de aprovação" e/ou "Pendente de aprovação de alteração de monitor".
- **Objetivo:** Validar que as indicações processadas (aprovadas ou rejeitadas) não são mais exibidas na lista de pendências.
- **Resultado esperado:** Após a aprovação ou rejeição de uma ou mais indicações, ao retornar à lista de pendências, apenas as indicações que ainda estão com status pendente são exibidas.
- **Tipo:** principal
- **Critérios cobertos:** AC4

### US08-CT05 — Tentativa de aprovação de indicação com status diferente de pendente
- **Pré-condição:** Admin está logado. Existe uma indicação de monitor que JÁ FOI processada (aprovada ou rejeitada anteriormente).
- **Objetivo:** Validar que o admin não consegue reprocessar uma indicação já concluída.
- **Resultado esperado:** O sistema impede a ação de aprovação ou rejeição para indicações que não possuem status pendente. A interface pode não apresentar as opções de aprovar/rejeitar ou exibir uma mensagem de erro.
- **Tipo:** segurança
- **Critérios cobertos:** a confirmar

### US08-CT06 — Aprovação de indicação para disciplina com monitor ativo (sem confirmação de troca)
- **Pré-condição:** Admin está logado. Existe uma indicação de alteração de monitor para uma disciplina que já possui um monitor ativo cadastrado. A indicação está com status "Pendente de aprovação de alteração de monitor".
- **Objetivo:** Validar o comportamento do sistema quando o admin tenta aprovar a alteração sem que a confirmação explícita da troca do monitor seja dada (se o fluxo exigir).
- **Resultado esperado:** O sistema deve apresentar a solicitação de confirmação para a troca do monitor antigo pelo novo. Se o admin não confirmar explicitamente, o vínculo do novo monitor não deve ser ativado e o monitor antigo deve permanecer ativo. A indicação pode permanecer pendente ou ser tratada como rejeitada implicitamente, dependendo do fluxo exato.
- **Tipo:** robustez
- **Critérios cobertos:** AC2

### US08-CT07 — Rejeição de indicação sem informar motivo
- **Pré-condição:** Admin está logado. Existe uma indicação de monitor com status "Pendente de aprovação".
- **Objetivo:** Validar o comportamento do sistema ao tentar rejeitar uma indicação sem fornecer um motivo.
- **Resultado esperado:** O sistema pode exigir que o motivo seja preenchido (exibindo uma mensagem de erro) ou registrar um motivo genérico (ex: "Não informado") se o campo for opcional. O vínculo muda para "Rejeitado".
- **Tipo:** robustez
- **Critérios cobertos:** AC3