### US08-CT01 — Aprovação de indicação de monitor para disciplina sem monitor
- **Pré-condição:** Um admin está logado. Existe uma indicação de monitor para uma disciplina com status "Pendente de aprovação". A disciplina não possui nenhum monitor ativo associado.
- **Objetivo:** Validar a aprovação de uma nova indicação de monitor para uma disciplina que ainda não tem monitor.
- **Resultado esperado:** O status do vínculo do monitor com a disciplina muda para "Ativo". O novo monitor ganha acesso de monitor para a disciplina.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US08-CT02 — Aprovação de alteração de monitor para disciplina já com monitor
- **Pré-condição:** Um admin está logado. Existe uma indicação de monitor para uma disciplina com status "Pendente de aprovação de alteração de monitor". A disciplina já possui um monitor ativo associado.
- **Objetivo:** Validar a aprovação da substituição de um monitor existente por um novo.
- **Resultado esperado:** O sistema exibe uma confirmação para o admin substituir o monitor antigo pelo novo. Após a confirmação do admin, o vínculo do novo monitor com a disciplina muda para "Ativo". Apenas o novo monitor passa a ter acesso como monitor da disciplina.
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US08-CT03 — Rejeição de indicação de monitor com motivo
- **Pré-condição:** Um admin está logado. Existe uma indicação de monitor com status "Pendente de aprovação".
- **Objetivo:** Validar a rejeição de uma indicação de monitor com o registro de um motivo.
- **Resultado esperado:** O status do vínculo do monitor com a disciplina muda para "Rejeitado". O motivo informado pelo admin é registrado no sistema associado à indicação.
- **Tipo:** principal
- **Critérios cobertos:** AC3

### US08-CT04 — Indicação processada (aprovada) removida da lista de pendências
- **Pré-condição:** Um admin está logado. Existe uma indicação de monitor com status "Pendente de aprovação".
- **Objetivo:** Validar que uma indicação aprovada deixa de ser exibida na lista de pendências.
- **Resultado esperado:** Após a aprovação da indicação, ao retornar para a lista de indicações pendentes, a indicação que foi processada não está mais visível.
- **Tipo:** principal
- **Critérios cobertos:** AC4

### US08-CT05 — Indicação processada (rejeitada) removida da lista de pendências
- **Pré-condição:** Um admin está logado. Existe uma indicação de monitor com status "Pendente de aprovação".
- **Objetivo:** Validar que uma indicação rejeitada deixa de ser exibida na lista de pendências.
- **Resultado esperado:** Após a rejeição da indicação, ao retornar para a lista de indicações pendentes, a indicação que foi processada não está mais visível.
- **Tipo:** principal
- **Critérios cobertos:** AC4

### US08-CT06 — Tentativa de aprovação de indicação com status diferente de "Pendente de aprovação" ou "Pendente de aprovação de alteração de monitor"
- **Pré-condição:** Um admin está logado. Existe uma indicação de monitor com um status diferente de "Pendente de aprovação" ou "Pendente de aprovação de alteração de monitor" (ex: "Ativo", "Rejeitado").
- **Objetivo:** Validar que o admin não consegue aprovar uma indicação que já foi processada.
- **Resultado esperado:** O sistema impede a ação de aprovação ou a opção de aprovação não está disponível para indicações com status que não sejam pendentes.
- **Tipo:** segurança
- **Critérios cobertos:** a confirmar

### US08-CT07 — Tentativa de rejeição de indicação com status diferente de "Pendente de aprovação"
- **Pré-condição:** Um admin está logado. Existe uma indicação de monitor com um status diferente de "Pendente de aprovação" (ex: "Ativo", "Rejeitado", "Pendente de aprovação de alteração de monitor").
- **Objetivo:** Validar que o admin não consegue rejeitar uma indicação que já foi processada ou que possui um status diferente do esperado para rejeição.
- **Resultado esperado:** O sistema impede a ação de rejeição ou a opção de rejeição não está disponível para indicações com status que não sejam "Pendente de aprovação".
- **Tipo:** segurança
- **Critérios cobertos:** a confirmar

### US08-CT08 — Aprovação de indicação de alteração de monitor sem confirmação pelo admin (cancelamento)
- **Pré-condição:** Um admin está logado. Existe uma indicação de monitor para uma disciplina com status "Pendente de aprovação de alteração de monitor", e a disciplina já possui um monitor ativo.
- **Objetivo:** Validar o cancelamento da aprovação de alteração de monitor quando o sistema solicita confirmação.
- **Resultado esperado:** Ao o admin escolher não confirmar a alteração após o aviso do sistema, o status do vínculo do antigo monitor permanece "Ativo" e o novo monitor não ganha acesso à disciplina. A indicação de alteração permanece em algum status pendente (a confirmar).
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US08-CT09 — Rejeição de indicação sem informar motivo (caso o campo seja opcional)
- **Pré-condição:** Um admin está logado. Existe uma indicação de monitor com status "Pendente de aprovação". O campo de motivo para rejeição é opcional.
- **Objetivo:** Validar a rejeição de uma indicação de monitor sem a obrigatoriedade de informar um motivo.
- **Resultado esperado:** O status do vínculo do monitor com a disciplina muda para "Rejeitado". O motivo registrado no sistema fica vazio ou nulo.
- **Tipo:** principal
- **Critérios cobertos:** AC3 (considerando o campo como opcional)

### US08-CT10 — Aprovação de indicação de monitor para disciplina que já tem monitor, mas a indicação é para um novo monitor (e não substituição)
- **Pré-condição:** Um admin está logado. Existe uma indicação de monitor para uma disciplina com status "Pendente de aprovação". A disciplina já possui um monitor ativo associado.
- **Objetivo:** Validar o comportamento do sistema quando uma nova indicação para uma disciplina já monitorada é feita sem ser explicitamente uma "alteração de monitor".
- **Resultado esperado:** O sistema deve tratar esta situação de acordo com a regra de negócio (a confirmar). Pode ser que a indicação seja tratada como a AC1 (permitindo múltiplos monitores), ou como a AC2 (forçando a substituição), ou rejeitada.
- **Tipo:** ambiguidade
- **Critérios cobertos:** a confirmar