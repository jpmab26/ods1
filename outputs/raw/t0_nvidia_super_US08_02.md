###US08-CT01 — Aprovação de indicação sem monitor existente  
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação" vinculada a uma disciplina que atualmente não possui monitor atribuído; o admin está autenticado e na tela de indicações pendentes.  
- **Objetivo:** Validar que a aprovação da indicação altera o vínculo para "Ativo" e concede ao aluno o acesso como monitor da disciplina.  
- **Resultado esperado:** Após o admin clicar em "Aprovar", o status da indicação muda para "Ativo", o aluno passa a ter permissões de monitor naquela disciplina e a indicação não aparece mais na lista de pendentes.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 1  

### US08-CT02 — Aprovação de indicação com monitor existente (confirmação de substituição)  
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação de alteração de monitor" vinculada a uma disciplina que já possui um monitor atribuído; o admin está autenticado e na tela de indicações pendentes.  
- **Objetivo:** Validar que, ao aprovar a indicação, o sistema solicita confirmação de substituição do monitor antigo e, ao confirmar, o vínculo passa para "Ativo" e somente o novo aluno obtém acesso como monitor.  
- **Resultado esperado:** Após o admin clicar em "Aprovar", o sistema exibe um diálogo de confirmação; ao aceitar, o status da indicação muda para "Ativo", o monitor anterior perde o acesso e o novo aluno passa a ter acesso como monitor da disciplina; a indicação some da lista de pendentes.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 2  

### US08-CT03 — Rejeição de indicação com motivo informado  
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação"; o admin está autenticado e na tela de indicações pendentes.  
- **Objetivo:** Validar que a rejeição da indicação, ao informar um motivo, altera o vínculo para "Rejeitado" e registra o motivo fornecido.  
- **Resultado esperado:** Após o admin clicar em "Rejeitar", preencher o campo de motivo e confirmar, o status da indicação muda para "Rejeitado", o motivo é salvo no histórico da indicação e a indicação não aparece mais na lista de pendentes.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 3  

### US08-CT04 — Indicação processada (aprovação) sai da lista de pendentes  
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação"; o admin está autenticado e na tela de indicações pendentes.  
- **Objetivo:** Garantir que, após aprovação, a indicação não permaneça listada entre as pendentes.  
- **Resultado esperado:** Depois que o admin aprova a indicação (conforme US08-CT01 ou US08-CT02, conforme o caso), ao retornar à lista de pendentes a indicação processada não está mais presente.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 4  

### US08-CT05 — Indicação processada (rejeição) sai da lista de pendentes  
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação"; o admin está autenticado e na tela de indicações pendentes.  
- **Objetivo:** Garantir que, após rejeição, a indicação não permaneça listada entre as pendentes.  
- **Resultado esperado:** Depois que o admin rejeita a indicação informando um motivo (conforme US08-CT03), ao retornar à lista de pendentes a indicação processada não está mais presente.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 4  

### US08-CT06 — Tentativa de aprovação sem confirmação na alteração de monitor (a confirmar)  
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação de alteração de monitor" vinculada a uma disciplina que já possui monitor atribuído; o admin está autenticado e na tela de indicações pendentes.  
- **Objetivo:** Verificar o comportamento do sistema quando o admin inicia a aprovação mas não confirma a substituição do monitor antigo.  
- **Resultado esperado:** **a confirmar** – Espera-se que o sistema mantenha a indicação com status "Pendente de aprovação de alteração de monitor" e não altere o vínculo nem o acesso dos monitores.  
- **Tipo:** alternativa  
- **Critérios cobertos:** a confirmar  

### US08-CT07 — Tentativa de rejeição sem informar motivo (a confirmar)  
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação"; o admin está autenticado e na tela de indicações pendentes.  
- **Objetivo:** Verificar o comportamento do sistema quando o admin tenta rejeitar a indicação sem preencher o campo de motivo.  
- **Resultado esperado:** **a confirmar** – Espera-se que o sistema impeça a rejeição e exija o preenchimento do motivo, mantendo a indicação com status "Pendente de aprovação".  
- **Tipo:** alternativa  
- **Critérios cobertos:** a confirmar