### US08-CT01 — Aprovar indicação de disciplina sem monitor
- **Pré-condição:** Admin logado; existe indicação com status "Pendente de aprovação" para disciplina sem monitor ativo
- **Objetivo:** Validar aprovação de nova monitoria para disciplina sem monitor
- **Resultado esperado:** Status muda para "Ativo"; aluno indicado ganha acesso como monitor da disciplina; indicação desaparece da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1, Cenário 4

### US08-CT02 — Aprovar alteração de monitor com confirmação
- **Pré-condição:** Admin logado; existe indicação com status "Pendente de aprovação de alteração de monitor" (disciplina já possui monitor ativo)
- **Objetivo:** Validar aprovação de troca de monitor com confirmação explícita
- **Resultado esperado:** Sistema solicita confirmação; ao confirmar, status muda para "Ativo"; novo aluno passa a ter acesso como monitor; monitor anterior perde acesso; indicação desaparece da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2, Cenário 4

### US08-CT03 — Cancelar aprovação de alteração de monitor
- **Pré-condição:** Admin logado; existe indicação com status "Pendente de aprovação de alteração de monitor"
- **Objetivo:** Validar cancelamento da troca de monitor na confirmação
- **Resultado esperado:** Sistema solicita confirmação; ao cancelar, indicação permanece com status "Pendente de aprovação de alteração de monitor" na lista; monitor atual mantém acesso
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2 (confirmação negada)

### US08-CT04 — Rejeitar indicação com motivo obrigatório
- **Pré-condição:** Admin logado; existe indicação com status "Pendente de aprovação"
- **Objetivo:** Validar rejeição com preenchimento de motivo
- **Resultado esperado:** Status muda para "Rejeitado"; motivo é registrado e visível; indicação desaparece da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3, Cenário 4

### US08-CT05 — Tentar rejeitar indicação sem informar motivo
- **Pré-condição:** Admin logado; existe indicação com status "Pendente de aprovação"
- **Objetivo:** Validar que motivo é obrigatório na rejeição
- **Resultado esperado:** Sistema impede rejeição sem motivo; exibe mensagem de erro/validação; indicação permanece com status "Pendente de aprovação" na lista
- **Tipo:** validação
- **Critérios cobertos:** Cenário 3 (a confirmar se motivo é obrigatório)

### US08-CT06 — Verificar remoção da lista após aprovação
- **Pré-condição:** Admin logado; lista de pendentes contém pelo menos uma indicação "Pendente de aprovação"
- **Objetivo:** Validar que indicação aprovada sai da fila de pendentes
- **Resultado esperado:** Após aprovar, ao retornar à lista, a indicação processada não é mais exibida
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT07 — Verificar remoção da lista após rejeição
- **Pré-condição:** Admin logado; lista de pendentes contém pelo menos uma indicação "Pendente de aprovação"
- **Objetivo:** Validar que indicação rejeitada sai da fila de pendentes
- **Resultado esperado:** Após rejeitar com motivo, ao retornar à lista, a indicação processada não é mais exibida
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT08 — Aprovar indicação já processada (não deve aparecer)
- **Pré-condição:** Admin logado; indicação foi aprovada ou rejeitada anteriormente
- **Objetivo:** Validar que indicações processadas não reaparecem na lista de pendentes
- **Resultado esperado:** Lista de pendentes não exibe indicações com status "Ativo" ou "Rejeitado"
- **Tipo:** regressão
- **Critérios cobertos:** Cenário 4

### US08-CT09 — Aprovar múltiplas indicações em sequência
- **Pré-condição:** Admin logado; lista de pendentes contém múltiplas indicações "Pendente de aprovação"
- **Objetivo:** Validar processamento sequencial sem perda de estado
- **Resultado esperado:** Cada aprovação atualiza status para "Ativo", remove item da lista e mantém as demais pendentes visíveis
- **Tipo:** carga
- **Critérios cobertos:** Cenário 1, Cenário 4

### US08-CT10 — Rejeitar indicação de alteração de monitor
- **Pré-condição:** Admin logado; existe indicação com status "Pendente de aprovação de alteração de monitor"
- **Objetivo:** Validar rejeição de troca de monitor
- **Resultado esperado:** Status muda para "Rejeitado"; motivo registrado; monitor atual mantém acesso; indicação desaparece da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3, Cenário 4 (aplicado a alteração)