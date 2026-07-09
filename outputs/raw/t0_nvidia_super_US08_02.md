### US08-CT01 — Aprovação de disciplina sem monitor
- **Pré-condição:** Admin visualiza indicação com status "Pendente de aprovação" vinculada a disciplina que não possui monitor atualmente
- **Objetivo:** Validar que a aprovação altera o vínculo para "Ativo" e concede acesso de monitor ao aluno
- **Resultado esperado:** Sistema muda o status da indicação para "Ativo" e o aluno passa a ter acesso como monitor da disciplina
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US08-CT02 — Aprovação de alteração de monitor com confirmação aceita
- **Pré-condição:** Admin visualiza indicação com status "Pendente de aprovação de alteração de monitor" vinculada a disciplina que já possui monitor atualmente
- **Objetivo:** Validar que, após confirmação, o sistema substitui o monitor antigo pelo novo e atualiza o vínculo para "Ativo"
- **Resultado esperado:** Sistema solicita confirmação; ao aceitar, muda o status da indicação para "Ativo", o novo aluno passa a ter acesso como monitor e o monitor anterior perde o acesso
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US08-CT03 — Aprovação de alteração de monitor com confirmação negada
- **Pré-condição:** Admin visualiza indicação com status "Pendente de aprovação de alteração de monitor" vinculada a disciplina que já possui monitor atualmente
- **Objetivo:** Verificar comportamento quando o admin nega a confirmação de substituição de monitor
- **Resultado esperado:** Sistema mantém o status da indicação como "Pendente de aprovação de alteração de monitor" e não altera o vínculo de monitor
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US08-CT04 — Rejeição com motivo informado
- **Pré-condição:** Admin visualiza indicação com status "Pendente de aprovação"
- **Objetivo:** Validar que a rejeição com motivo registra o motivo e altera o status para "Rejeitado"
- **Resultado esperado:** Sistema muda o status da indicação para "Rejeitado" e salva o motivo informado
- **Tipo:** principal
- **Critérios cobertos:** AC3

### US08-CT05 — Rejeição sem motivo (campo obrigatório)
- **Pré-condição:** Admin visualiza indicação com status "Pendente de aprovação" e tenta rejeitar sem preencher o campo de motivo
- **Objetivo:** Verificar se o sistema impede a rejeição quando o motivo não é informado
- **Resultado esperado:** Sistema bloqueia a ação de rejeição e exibe mensagem indicando que o motivo é obrigatório
- **Tipo:** de erro
- **Critérios cobertos:** a confirmar

### US08-CT06 — Indicação processada (aprovação) sai da lista de pendentes
- **Pré-condição:** Admin aprova uma indicação com status "Pendente de aprovação" (disciplina sem monitor)
- **Objetivo:** Garantir que, após o processamento, a indicação não apareça mais na lista de pendentes
- **Resultado esperado:** Ao retornar à lista de indicações pendentes, a indicação aprovada não está presente
- **Tipo:** principal
- **Critérios cobertos:** AC4

### US08-CT07 — Indicação processada (rejeição) sai da lista de pendentes
- **Pré-condição:** Admin rejeita uma indicação com status "Pendente de aprovação", informando motivo
- **Objetivo:** Garantir que, após o processamento, a indicação não apareça mais na lista de pendentes
- **Resultado esperado:** Ao retornar à lista de indicações pendentes, a indicação rejeitada não está presente
- **Tipo:** principal
- **Critérios cobertos:** AC4

### US08-CT08 — Tentativa de aprovação de indicação já processada (status Ativo)
- **Pré-condição:** Admin visualiza indicação com status "Ativo" (já aprovada anteriormente)
- **Objetivo:** Verificar se o sistema impede nova aprovação de uma indicação já ativa
- **Resultado esperado:** Sistema não permite a ação de aprovação e exibe mensagem indicando que a indicação já está processada
- **Tipo:** de erro
- **Critérios cobertos:** a confirmar

### US08-CT09 — Tentativa de rejeição de indicação já processada (status Rejeitado)
- **Pré-condição:** Admin visualiza indicação com status "Rejeitado"
- **Objetivo:** Verificar se o sistema impede nova rejeição de uma indicação já rejeitada
- **Resultado esperado:** Sistema não permite a ação de rejeição e exibe mensagem indicando que a indicação já está processada
- **Tipo:** de erro
- **Critérios cobertos:** a confirmar

### US08-CT10 — Tentativa de aprovação com status inválido (ex: "Em análise")
- **Pré-condição:** Admin visualiza indicação com status não previsto nos critérios de aceitação (ex: "Em análise")
- **Objetivo:** Verificar comportamento do sistema diante de status inesperado na tela de indicação
- **Resultado esperado:** Sistema exibe mensagem de erro indicando que o status não permite a operação de aprovação/rejeição
- **Tipo:** de erro
- **Critérios cobertos:** a confirmar