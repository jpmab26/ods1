###US08-CT01 — Aprovação de disciplina sem monitor (status Pendente de aprovação)
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação" vinculada a uma disciplina que ainda não possui monitor ativo; admin está autenticado e na lista de pendências.
- **Objetivo:** Verificar que a aprovação altera o status para "Ativo" e concede ao aluno o acesso como monitor da disciplina.
- **Resultado esperado:** Após a ação de aprovar, o vínculo da indicação passa a ter status "Ativo" e o aluno passa a ter permissão de monitor naquela disciplina.
- **Tipo:** principal
- **Critérios cobertos:** AC1 (Cenário 1)

### US08-CT02 — Aprovação de disciplina com monitor existente (confirmação aceita)
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação de alteração de monitor" para uma disciplina que já possui um monitor ativo (monitor antigo); admin está autenticado e na lista de pendências.
- **Objetivo:** Validar que, ao aprovar a alteração e confirmar a substituição, o monitor antigo perde o acesso e o novo monitor passa a ter status "Ativo".
- **Resultado esperado:** Após aprovação e confirmação, o sistema exibe mensagem de confirmação; ao aceitar, o vínculo da nova indicação fica "Ativo", o antigo passa a "Inativo" (ou removido) e apenas o novo aluno tem acesso como monitor da disciplina.
- **Tipo:** principal
- **Critérios cobertos:** AC2 (Cenário 2)

### US08-CT03 — Aprovação de disciplina com monitor existente (confirmação cancelada)
- **Pré-condição:** Mesmo que US08-CT02.
- **Objetivo:** Verificar que, se o admin cancelar a confirmação de substituição, nenhum vínculo é alterado.
- **Resultado esperado:** Após a ação de aprovar e escolher "Cancelar" na confirmação, o status da indicação permanece "Pendente de aprovação de alteração de monitor", o monitor antigo continua ativo e nenhum novo acesso é concedido.
- **Tipo:** alternativa
- **Critérios cobertos:** AC2 (a confirmar – comportamento de cancelamento não especificado)

### US08-CT04 — Rejeição de indicação com motivo informado
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação"; admin está autenticado e na lista de pendências.
- **Objetivo:** Assegurar que a rejeição com motivo registra o motivo e altera o status para "Rejeitado".
- **Resultado esperado:** Após rejeitar e preencher o campo de motivo, o vínculo passa a ter status "Rejeitado" e o motivo informado é persistido e visível na indicação.
- **Tipo:** principal
- **Critérios cobertos:** AC3 (Cenário 3)

### US08-CT05 — Rejeição de indicação sem motivo (campo obrigatório vazio)
- **Pré-condição:** Mesmo que US08-CT04.
- **Objetivo:** Verificar comportamento quando o admin tenta rejeitar sem preencher o motivo (se o campo for obrigatório).
- **Resultado esperado:** O sistema impede a rejeição e exibe mensagem de validação informando que o motivo é obrigatório; o status da indicação permanece "Pendente de aprovação".
- **Tipo:** alternativa
- **Critérios cobertos:** AC3 (a confirmar – obrigatoriedade do motivo não explicitada)

### US08-CT06 — Indicação processada (aprovada) não aparece mais na lista de pendências
- **Pré-condição:** Existe uma indicação com status "Pendente de aprovação"; admin está na lista de pendências.
- **Objetivo:** Confirmar que, após aprovação, a indicação some da lista de pendências.
- **Resultado esperado:** Após aprovar a indicação e retornar à lista de pendências, a indicação aprovada não é mais exibida.
- **Tipo:** principal
- **Critérios cobertos:** AC4 (Cenário 4)

### US08-CT07 — Indicação processada (rejeitada) não aparece mais na lista de pendências
- **Pré-condição:** Mesmo que US08-CT06, mas a ação será rejeição com motivo.
- **Objetivo:** Confirmar que, após rejeição, a indicação some da lista de pendências.
- **Resultado esperado:** Após rejeitar a indicação e retornar à lista de pendências, a indicação rejeitada não é mais exibida.
- **Tipo:** principal
- **Critérios cobertos:** AC4 (Cenário 4)

### US08-CT08 — Tentativa de aprovação de indicação já processada (status Ativo)
- **Pré-condição:** Existe uma indicação com status "Ativo" (já aprovada anteriormente); admin está na lista de pendências (ou visualizando a indicação através de busca).
- **Objetivo:** Verificar que o sistema não permite reprovar uma indicação já ativa ou trata a ação como inválida.
- **Resultado esperado:** Ao tentar aprovar novamente, o sistema exibe mensagem de erro ou aviso indicando que a indicação já está processada e não altera o status.
- **Tipo:** alternativa
- **Critérios cobertos:** a confirmar (regra não especificada na US)

### US08-CT09 — Tentativa de rejeição de indicação já processada (status Rejeitado)
- **Pré-condição:** Existe uma indicação com status "Rejeitado"; admin está visualizando a indicação.
- **Objetivo:** Verificar que o sistema não permite rejeitar novamente uma indicação já rejeitada.
- **Resultado esperado:** Ao tentar rejeitar novamente, o sistema exibe mensagem de erro ou aviso e não altera o status nem registra novo motivo.
- **Tipo:** alternativa
- **Critérios cobertos:** a confirmar (regra não especificada na US)