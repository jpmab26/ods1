### US08-CT01 — Aprovação de indicação para disciplina sem monitor atual
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação" para disciplina que não possui monitor ativo
- **Objetivo:** Validar aprovação de nova monitoria para disciplina vaga
- **Resultado esperado:** Status da indicação muda para "Ativo"; aluno indicado ganha acesso como monitor da disciplina; indicação removida da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1, Cenário 4

### US08-CT02 — Aprovação de indicação para disciplina com monitor ativo (confirma substituição)
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação de alteração de monitor" para disciplina que já possui monitor ativo
- **Objetivo:** Validar aprovação de troca de monitor com confirmação
- **Resultado esperado:** Sistema solicita confirmação da substituição; ao confirmar, status muda para "Ativo"; novo aluno ganha acesso como monitor; monitor anterior perde acesso à disciplina; indicação removida da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2, Cenário 4

### US08-CT03 — Aprovação de indicação para disciplina com monitor ativo (cancela substituição)
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação de alteração de monitor" para disciplina que já possui monitor ativo
- **Objetivo:** Validar cancelamento da troca de monitor na confirmação
- **Resultado esperado:** Sistema solicita confirmação; ao cancelar, indicação permanece com status "Pendente de aprovação de alteração de monitor"; monitor atual mantém acesso; indicação permanece na lista de pendentes
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2 (confirmação negativa), Cenário 4 (não processada)

### US08-CT04 — Rejeição de indicação com motivo informado
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação" (disciplina sem monitor ou com monitor — regra não especificada, assumir ambos)
- **Objetivo:** Validar rejeição com registro de motivo
- **Resultado esperado:** Status da indicação muda para "Rejeitado"; motivo informado é registrado; aluno não ganha acesso como monitor; indicação removida da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3, Cenário 4

### US08-CT05 — Tentativa de rejeição sem informar motivo
- **Pré-condição:** Admin autenticado; existe indicação com status "Pendente de aprovação"
- **Objetivo:** Validar exigência de motivo na rejeição
- **Resultado esperado:** Sistema impede rejeição sem motivo; exibe mensagem de erro/validação; indicação permanece com status original na lista de pendentes
- **Tipo:** validação
- **Critérios cobertos:** Cenário 3 (a confirmar — regra de obrigatoriedade do motivo não explicitada, mas implícita)

### US08-CT06 — Visualização de lista de pendentes após processar múltiplas indicações
- **Pré-condição:** Admin autenticado; lista de pendentes contém múltiplas indicações (ex.: 3 pendentes)
- **Objetivo:** Validar remoção individual de indicações processadas da lista
- **Resultado esperado:** Após aprovar/rejeitar uma indicação e retornar à lista, apenas a processada é removida; as demais permanecem visíveis com seus respectivos status
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT07 — Aprovação de indicação onde aluno já é monitor de outra disciplina
- **Pré-condição:** Admin autenticado; existe indicação "Pendente de aprovação" para aluno que já é monitor ativo em outra disciplina
- **Objetivo:** Validar se sistema permite aluno ser monitor de múltiplas disciplinas
- **Resultado esperado:** Status muda para "Ativo"; aluno passa a ter acesso também na nova disciplina; indicação removida da lista de pendentes
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1 (a confirmar — regra de exclusividade de monitoria não documentada)

### US08-CT08 — Aprovação de indicação para disciplina onde aluno já é monitor (mesma disciplina)
- **Pré-condição:** Admin autenticado; existe indicação "Pendente de aprovação" para aluno que já consta como monitor ativo da mesma disciplina (duplicidade)
- **Objetivo:** Validar tratamento de indicação duplicada para mesma disciplina/aluno
- **Resultado esperado:** Sistema impede aprovação ou ignora duplicidade; exibe mensagem apropriada; indicação permanece ou é removida conforme regra
- **Tipo:** validação
- **Critérios cobertos:** Cenário 1 (a confirmar — cenário não previsto nos critérios)

### US08-CT09 — Acesso do aluno aprovado às funcionalidades de monitor
- **Pré-condição:** Indicação aprovada (status "Ativo") via US08-CT01 ou US08-CT02; aluno faz login no sistema
- **Objetivo:** Validar concessão efetiva de acesso ao papel de monitor
- **Resultado esperado:** Aluno visualiza/acessa funcionalidades de monitor (agendamentos, presenças, etc.) para a disciplina aprovada
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1 ("passa a ter acesso como monitor"), Cenário 2 ("apenas o aluno novo passa a ter acesso")

### US08-CT10 — Remoção de acesso do monitor anterior após substituição aprovada
- **Pré-condição:** Substituição aprovada via US08-CT02; monitor anterior faz login no sistema
- **Objetivo:** Validar revogação de acesso do monitor substituído
- **Resultado esperado:** Monitor anterior não possui mais acesso às funcionalidades de monitor para a disciplina substituída
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2 ("apenas o aluno novo passa a ter acesso")

### US08-CT11 — Persistência do motivo de rejeição no histórico
- **Pré-condição:** Indicação rejeitada via US08-CT04 com motivo "X"
- **Objetivo:** Validar que motivo fica registrado e consultável
- **Resultado esperado:** Ao consultar detalhes/histórico da indicação rejeitada, o motivo "X" é exibido corretamente
- **Tipo:** validação
- **Critérios cobertos:** Cenário 3 ("motivo é registrado")