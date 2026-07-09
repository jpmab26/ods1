### US08-CT01 — Aprovar indicação quando disciplina ainda não tem monitor
- **Pré‑condição:** Admin autenticado; indicação de monitoramento exibida com status “Pendente de aprovação”; disciplina ainda não possui monitor associado.
- **Objetivo:** Verificar que a aprovação cria vínculo ativo e concede acesso ao monitor.
- **Resultado esperado:** Ao clicar em “Aprovar”, o vínculo passa para “Ativo” e o aluno passa a ter acesso como monitor da disciplina; a indicação desaparece da lista de pendentes.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US08-CT02 — Aprovar indicação quando disciplina já tem monitor (confirmação aceita)
- **Pré‑condição:** Admin autenticado; indicação exibida com status “Pendente de aprovação de alteração de monitor”; disciplina já possui um monitor ativo.
- **Objetivo:** Confirmar que a aprovação substitui o monitor antigo pelo novo após confirmação positiva.
- **Resultado esperado:** Sistema exibe mensagem de confirmação; admin aceita; vínculo do monitor antigo é desativado, vínculo do novo monitor passa para “Ativo”; somente o novo monitor tem acesso; a indicação sai da fila de pendentes.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2

### US08-CT03 — Aprovar indicação quando disciplina já tem monitor (confirmação rejeitada)
- **Pré‑condição:** Admin autenticado; indicação com status “Pendente de aprovação de alteração de monitor”; disciplina já possui monitor.
- **Objetivo:** Verificar o comportamento quando o admin cancela a substituição na tela de confirmação.
- **Resultado esperado:** Ao escolher “Cancelar”/“Não” na confirmação, o vínculo permanece inalterado, o monitor antigo continua ativo, a indicação permanece com status “Pendente de aprovação de alteração de monitor” e continua na lista de pendentes.
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar (confirmação de alteração de monitor)

### US08-CT04 — Rejeitar indicação informando motivo
- **Pré‑condição:** Admin autenticado; indicação exibida com status “Pendente de aprovação”; campo “Motivo da rejeição” disponível.
- **Objetivo:** Garantir que a rejeição registra o motivo e muda o status da indicação.
- **Resultado esperado:** Admin preenche o motivo e confirma a rejeição; vínculo muda para “Rejeitado”, o motivo é armazenado e exibido no histórico da indicação; a indicação sai da lista de pendentes.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3

### US08-CT05 — Rejeitar indicação sem preencher motivo
- **Pré‑condição:** Admin autenticado; indicação em status “Pendente de aprovação”.
- **Objetivo:** Avaliar a restrição de preenchimento obrigatório do motivo ao rejeitar.
- **Resultado esperado:** Ao tentar rejeitar sem informar motivo, o sistema impede a ação e exibe mensagem de validação solicitando o preenchimento do campo; o status da indicação permanece “Pendente de aprovação”.
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar (validação de campo motivo)

### US08-CT06 — Aprovar indicação já com status diferente de pendente
- **Pré‑condição:** Admin autenticado; indicação exibida com status “Ativo” ou “Rejeitado”.
- **Objetivo:** Verificar que a ação de aprovação não está disponível para indicações que não estejam pendentes.
- **Resultado esperado:** Botão/ação “Aprovar” está desabilitado ou oculto; tentativa de acesso direto à URL de aprovação retorna erro ou redirecionamento para página de erros/alerta.
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar (restrição de ação por status)

### US08-CT07 — Rejeitar indicação já com status diferente de pendente
- **Pré‑condição:** Admin autenticado; indicação com status “Ativo” ou “Rejeitado”.
- **Objetivo:** Garantir que a ação de rejeição não pode ser executada fora do fluxo pendente.
- **Resultado esperado:** Botão/ação “Rejeitar” está desabilitado ou oculta; tentativa direta à URL de rejeição gera erro ou mensagem de operação inválida.
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar (restrição de ação por status)

### US08-CT08 — Indic ação processada permanece invisível após navegação
- **Pré‑condição:** Admin autenticado; indicação foi aprovada ou rejeitada com sucesso.
- **Objetivo:** Confirmar que a indicação processada não reaparece na lista de pendentes ao retornar à página.
- **Resultado esperado:** Ao clicar em “Voltar à lista de pendentes” ou recarregar a página, a indicação não consta mais no grid/lista de itens pendentes.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT09 — Concorrência: dois admins aprovam a mesma indicação simultaneamente
- **Pré‑condição:** Dois administradores autenticados; mesma indicação em status “Pendente de aprovação” visível para ambos.
- **Objetivo:** Verificar o controle de concorrência ao aprovar simultaneamente.
- **Resultado esperado:** O primeiro admin que confirmar a aprovação gera vínculo “Ativo”; ao segundo admin tentar aprovar, o sistema informa que a indicação já foi processada e não permite duplicidade; a indicação desaparece da lista para ambos.
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar (concorrência)

### US08-CT10 — Concorrência: admin aprova enquanto outro rejeita
- **Pré‑condição:** Dois administradores autenticados; mesma indicação pendente.
- **Objetivo:** Garantir que apenas a primeira ação (aprovar ou rejeitar) é efetivada.
- **Resultado esperado:** A primeira ação concluída altera o status (para “Ativo” ou “Rejeitado”); a segunda ação recebe mensagem de que a indicação já foi processada e não altera o estado.
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar (concorrência)