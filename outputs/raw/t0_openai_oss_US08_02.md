### US08-CT01 — Aprovar indicação quando disciplina não possui monitor  
- **Pré‑condição:** Admin autenticado; indicação exibida com status **“Pendente de aprovação”**; disciplina sem monitor cadastrado.  
- **Objetivo:** Verificar que ao aprovar a indicação o vínculo da disciplina passa para “Ativo” e o aluno indicado obtém acesso como monitor.  
- **Resultado esperado:** Sistema altera o status da indicação para “Ativo”, cria o vínculo monitor‑disciplina e o novo monitor consegue acessar as funcionalidades de monitor da disciplina.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 1  

### US08-CT02 — Aprovar indicação quando disciplina já tem monitor (confirmação aceita)  
- **Pré‑condição:** Admin autenticado; indicação exibida com status **“Pendente de aprovação de alteração de monitor”**; disciplina já possui monitor antigo.  
- **Objetivo:** Validar o fluxo de aprovação de troca de monitor com confirmação positiva.  
- **Resultado esperado:** Sistema exibe pergunta de confirmação; admin confirma; status da indicação muda para “Ativo”, vínculo do monitor antigo é desativado e o novo monitor passa a ter acesso exclusivo como monitor da disciplina.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 2  

### US08-CT03 — Aprovar indicação quando disciplina já tem monitor (confirmação recusada)  
- **Pré‑condição:** Admin autenticado; indicação com status **“Pendente de aprovação de alteração de monitor”**; disciplina com monitor antigo.  
- **Objetivo:** Verificar o comportamento quando o admin cancela a troca de monitor.  
- **Resultado esperado:** Sistema exibe pergunta de confirmação; admin recusa; indicação permanece com status “Pendente de aprovação de alteração de monitor” e nenhum vínculo é alterado.  
- **Tipo:** alternativo  
- **Critérios cobertos:** a confirmar (confirmação recusada não explicitada na US)  

### US08-CT04 — Rejeitar indicação informando motivo (status pendente padrão)  
- **Pré‑condição:** Admin autenticado; indicação exibida com status **“Pendente de aprovação”**.  
- **Objetivo:** Confirmar que a rejeição grava o motivo e altera o status para “Rejeitado”.  
- **Resultado esperado:** Admin preenche campo “Motivo da rejeição”, confirma rejeição; sistema grava o motivo, altera o status da indicação para “Rejeitado” e exibe o motivo nas informações da indicação.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 3  

### US08-CT05 — Rejeitar indicação sem informar motivo (campo opcional?)  
- **Pré‑condição:** Admin autenticado; indicação com status **“Pendente de aprovação”**.  
- **Objetivo:** Avaliar o que ocorre se o admin tenta rejeitar sem preencher o motivo.  
- **Resultado esperado:** **Critério a confirmar** – se o campo é obrigatório, o sistema impede a ação exibindo mensagem de validação; caso contrário, a indicação recebe status “Rejeitado” com motivo vazio.  
- **Tipo:** alternativo  
- **Critérios cobertos:** a confirmar  

### US08-CT06 — Indicação aprovada deixa de aparecer na lista de pendentes  
- **Pré‑condição:** Admin autenticado; lista de indicações pendentes contendo a indicação que será aprovada.  
- **Objetivo:** Garantir que, após aprovação, a indicação não permanece na fila de pendentes.  
- **Resultado esperado:** Admin aprova a indicação; após retorno à lista, a indicação não está mais presente.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 4  

### US08-CT07 — Indicação rejeitada deixa de aparecer na lista de pendentes  
- **Pré‑condição:** Admin autenticado; lista de indicações pendentes contendo a indicação que será rejeitada.  
- **Objetivo:** Verificar que, após rejeição, a indicação é removida da fila de pendentes.  
- **Resultado esperado:** Admin rejeita (com motivo); ao voltar à lista, a indicação não aparece mais.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 4  

### US08-CT08 — Acesso à página de aprovação por usuário não‑admin  
- **Pré‑condição:** Usuário autenticado com perfil diferente de admin (ex.: monitor ou estudante).  
- **Objetivo:** Garantir que apenas admins podem visualizar e executar ações de aprovação/rejeição.  
- **Resultado esperado:** Sistema impede acesso, exibindo mensagem de “Acesso negado” ou redirecionando para página de erro.  
- **Tipo:** alternativo  
- **Critérios cobertos:** a confirmar (restrição de papéis não explicitada na US)  

### US08-CT09 — Indicação com status inválido na fila (ex.: “Ativo”)  
- **Pré‑condição:** Admin autenticado; indicação aparece erroneamente na lista com status **“Ativo”**.  
- **Objetivo:** Testar robustez ao tentar aprovar/rejeitar indicação já processada.  
- **Resultado esperado:** Sistema não permite ação e informa que a indicação já está processada.  
- **Tipo:** alternativo  
- **Critérios cobertos:** a confirmar  

### US08-CT10 — Falha na gravação no banco ao aprovar  
- **Pré‑condição:** Admin autenticado; indicação pendente válida; simulação de falha de conexão MySQL antes da commit.  
- **Objetivo:** Verificar comportamento em caso de erro de persistência.  
- **Resultado esperado:** Sistema apresenta mensagem de erro de processamento, mantém a indicação em status “Pendente de aprovação” e não cria vínculo de monitor.  
- **Tipo:** erro  
- **Critérios cobertos:** a confirmar (tratamento de exceções não descrito)