### US08-CT01 — Aprovação de indicação para disciplina sem monitor (caminho principal)
- **Pré-condição:** Existe indicação com status "Pendente de aprovação" para disciplina que não possui monitor ativo; admin autenticado
- **Objetivo:** Validar aprovação simples de nova indicação
- **Resultado esperado:** Status muda para "Ativo"; aluno indicado ganha acesso como monitor da disciplina; indicação removida da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1, Cenário 4

### US08-CT02 — Aprovação de indicação para disciplina com monitor — confirmação de substituição
- **Pré-condição:** Existe indicação com status "Pendente de aprovação de alteração de monitor" para disciplina que já possui monitor ativo; admin autenticado
- **Objetivo:** Validar aprovação com confirmação de troca de monitor
- **Resultado esperado:** Sistema exibe confirmação; ao confirmar, status muda para "Ativo"; novo aluno ganha acesso como monitor; monitor anterior perde acesso; indicação removida da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2, Cenário 4

### US08-CT03 — Aprovação de indicação para disciplina com monitor — cancelamento na confirmação
- **Pré-condição:** Existe indicação com status "Pendente de aprovação de alteração de monitor" para disciplina com monitor ativo; admin autenticado
- **Objetivo:** Validar que cancelar na confirmação mantém estado original
- **Resultado esperado:** Sistema exibe confirmação; ao cancelar, status permanece "Pendente de aprovação de alteração de monitor"; monitor atual mantém acesso; indicação permanece na lista de pendentes
- **Tipo:** alternativa
- **Critérios cobertos:** Cenário 2 (confirmação negada), Cenário 4 (não sai da fila)

### US08-CT04 — Rejeição de indicação com motivo válido
- **Pré-condição:** Existe indicação com status "Pendente de aprovação" (ou "Pendente de aprovação de alteração de monitor"); admin autenticado
- **Objetivo:** Validar rejeição com registro de motivo
- **Resultado esperado:** Status muda para "Rejeitado"; motivo informado é salvo; indicação removida da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3, Cenário 4

### US08-CT05 — Rejeição de indicação sem informar motivo
- **Pré-condição:** Existe indicação com status "Pendente de aprovação"; admin autenticado
- **Objetivo:** Verificar comportamento quando motivo não é preenchido (campo obrigatório?)
- **Resultado esperado:** Sistema impede rejeição sem motivo e exibe mensagem de validação; status permanece inalterado; indicação continua na lista de pendentes
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar

### US08-CT06 — Verificação de remoção da fila após aprovação
- **Pré-condição:** Lista de pendentes contém uma ou mais indicações; admin aprova uma delas (CT01 ou CT02)
- **Objetivo:** Confirmar que indicação processada não aparece mais na lista de pendentes
- **Resultado esperado:** Ao retornar à lista, a indicação aprovada não é exibida; demais pendentes permanecem
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT07 — Verificação de remoção da fila após rejeição
- **Pré-condição:** Lista de pendentes contém uma ou mais indicações; admin rejeita uma delas com motivo (CT04)
- **Objetivo:** Confirmar que indicação rejeitada não aparece mais na lista de pendentes
- **Resultado esperado:** Ao retornar à lista, a indicação rejeitada não é exibida; demais pendentes permanecem
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT08 — Aprovação de indicação já processada (idempotência)
- **Pré-condição:** Indicação já está com status "Ativo" ou "Rejeitado"; admin tenta aprovar novamente via ação direta (ex.: URL direta, botão reabilitado)
- **Objetivo:** Validar que sistema impede nova ação sobre indicação finalizada
- **Resultado esperado:** Sistema não permite nova aprovação; exibe mensagem de erro ou ignora ação; status permanece inalterado
- **Tipo:** exceção
- **Critérios cobertos:** a confirmar

### US08-CT09 — Aprovação simultânea de múltiplas indicações para mesma disciplina
- **Pré-condição:** Duas indicações "Pendente de aprovação" para a mesma disciplina (sem monitor); admin aprova a primeira
- **Objetivo:** Verificar comportamento quando segunda indicação é aprovada após a primeira tornar a disciplina com monitor
- **Resultado esperado:** Primeira aprovação segue CT01; segunda indicação, ao ser aprovada, deve seguir fluxo de "alteração de monitor" (confirmação de substituição) conforme Cenário 2
- **Tipo:** borda
- **Critérios cobertos:** Cenário 1, Cenário 2 (transição de estado), a confirmar

### US08-CT10 — Rejeição de indicação de alteração de monitor
- **Pré-condição:** Indicação com status "Pendente de aprovação de alteração de monitor"; admin rejeita com motivo
- **Objetivo:** Validar rejeição específica para mudança de monitor
- **Resultado esperado:** Status muda para "Rejeitado"; motivo registrado; monitor atual mantém acesso; indicação removida da lista de pendentes
- **Tipo:** alternativa
- **Critérios cobertos:** Cenário 3, Cenário 4 (aplicado a alteração)