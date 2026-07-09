### US08-CT01 — Aprovação de indicação para disciplina sem monitor
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação" para disciplina sem monitor atual
- **Objetivo:** Validar aprovação simples de nova monitoria
- **Resultado esperado:** Vínculo muda para "Ativo"; aluno indicado passa a ter acesso como monitor da disciplina
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US08-CT02 — Aprovação de indicação para disciplina com monitor — confirma substituição
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação de alteração de monitor" (disciplina já possui monitor ativo)
- **Objetivo:** Validar fluxo de substituição de monitor com confirmação positiva
- **Resultado esperado:** Sistema exibe confirmação; ao aceitar, vínculo muda para "Ativo"; apenas o novo aluno passa a ter acesso como monitor; monitor anterior perde acesso
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2

### US08-CT03 — Aprovação de indicação para disciplina com monitor — cancela substituição
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação de alteração de monitor"
- **Objetivo:** Validar cancelamento da substituição quando admin não confirma
- **Resultado esperado:** Sistema exibe confirmação; ao cancelar, indicação permanece com status "Pendente de aprovação de alteração de monitor"; monitor atual mantém acesso
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2

### US08-CT04 — Rejeição de indicação com motivo válido
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação"
- **Objetivo:** Validar rejeição com registro de motivo
- **Resultado esperado:** Vínculo muda para "Rejeitado"; motivo informado é registrado e visível no histórico
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3

### US08-CT05 — Rejeição de indicação sem informar motivo
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação"
- **Objetivo:** Validar obrigatoriedade do motivo na rejeição
- **Resultado esperado:** Sistema impede a rejeição e exibe mensagem de erro solicitando o motivo
- **Tipo:** negativo
- **Critérios cobertos:** Cenário 3 (a confirmar)

### US08-CT06 — Indicação aprovada sai da lista de pendentes
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação" na lista
- **Objetivo:** Verificar remoção da indicação processada (aprovação) da fila
- **Resultado esperado:** Após aprovar, ao retornar à lista de pendentes, a indicação não aparece mais
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT07 — Indicação rejeitada sai da lista de pendentes
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação" na lista
- **Objetivo:** Verificar remoção da indicação processada (rejeição) da fila
- **Resultado esperado:** Após rejeitar com motivo, ao retornar à lista de pendentes, a indicação não aparece mais
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT08 — Tentativa de aprovar indicação já processada
- **Pré-condição:** Admin autenticado; indicação já foi aprovada ou rejeitada anteriormente (status "Ativo" ou "Rejeitado")
- **Objetivo:** Validar proteção contra reprocessamento
- **Resultado esperado:** Sistema não permite nova ação de aprovação/rejeição; exibe mensagem de que indicação já foi processada
- **Tipo:** negativo
- **Critérios cobertos:** Cenário 4 (a confirmar)

### US08-CT09 — Visualização de detalhes da indicação antes da decisão
- **Pré-condição:** Admin autenticado; lista de pendentes contém indicações com diferentes status
- **Objetivo:** Verificar se admin consegue ver detalhes (aluno, disciplina, status, data) antes de aprovar/rejeitar
- **Resultado esperado:** Ao clicar na indicação, são exibidos dados completos para subsidiar a decisão
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 1, Cenário 2, Cenário 3

### US08-CT10 — Aprovação de múltiplas indicações em sequência
- **Pré-condição:** Admin autenticado; lista de pendentes contém várias indicações com status "Pendente de aprovação"
- **Objetivo:** Validar processamento consecutivo sem perda de estado
- **Resultado esperado:** Cada aprovação atualiza status para "Ativo", remove da lista e mantê as demais pendentes intactas
- **Tipo:** borda
- **Critérios cobertos:** Cenário 1, Cenário 4

### US08-CT11 — Verificação de acesso do novo monitor após aprovação de substituição
- **Pré-condição:** Admin aprovou substituição de monitor (Cenário 2 confirmado); novo aluno e antigo monitor existem no sistema
- **Objetivo:** Confirmar mudança efetiva de permissões de acesso
- **Resultado esperado:** Novo aluno consegue acessar funcionalidades de monitor da disciplina; antigo monitor não consegue mais acessar
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2