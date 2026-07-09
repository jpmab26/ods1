### US08-CT01 — Aprovar indicação de disciplina sem monitor (caminho feliz)
- **Pré‑condição:** Admin autenticado; indicação encontrada com status **“Pendente de aprovação”**; disciplina ainda não possui monitor associado.
- **Objetivo:** Verificar que a aprovação cria o vínculo “Ativo” e concede acesso ao monitor.
- **Resultado esperado:** Sistema altera o status da indicação para **“Ativo”**, cria vínculo monitor‑disciplina, e o aluno passa a ter permissões de monitor na disciplina. A indicação desaparece da lista de pendentes.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US08-CT02 — Aprovar indicação de disciplina com monitor (caminho feliz – aceitação da troca)
- **Pré‑condição:** Admin autenticado; indicação encontrada com status **“Pendente de aprovação de alteração de monitor”**; disciplina já possui monitor (monitor antigo) cadastrado.
- **Objetivo:** Garantir que a aprovação solicita confirmação e, ao aceitar, substitui o monitor antigo pelo novo.
- **Resultado esperado:** Sistema exibe caixa de diálogo de confirmação; ao confirmar, altera o vínculo para **“Ativo”** atribuindo o novo aluno como monitor, desativa o vínculo do monitor antigo e registra a troca. A indicação desaparece da fila de pendentes.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2

### US08-CT03 — Aprovar indicação de disciplina com monitor (caminho alternativo – recusa da troca)
- **Pré‑condição:** Admin autenticado; indicação com status **“Pendente de aprovação de alteração de monitor”**; disciplina já tem monitor.
- **Objetivo:** Verificar o comportamento quando o admin cancela a confirmação da troca.
- **Resultado esperado:** Sistema mantém o vínculo antigo, a indicação permanece com status **“Pendente de aprovação de alteração de monitor”** (não é removida da fila), e nenhuma alteração de acesso ocorre.
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2 (a confirmar – fluxo de recusa)

### US08-CT04 — Rejeitar indicação fornecendo motivo (caminho feliz)
- **Pré‑condição:** Admin autenticado; indicação com status **“Pendente de aprovação”**.
- **Objetivo:** Confirmar que a rejeição altera o status e grava o motivo informado.
- **Resultado esperado:** Sistema muda o status da indicação para **“Rejeitado”**, armazena o texto do motivo associado ao registro, e a indicação deixa a lista de pendentes.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3

### US08-CT05 — Rejeitar indicação sem informar motivo (campo opcional)
- **Pré‑condição:** Admin autenticado; indicação com status **“Pendente de aprovação”**.
- **Objetivo:** Avaliar o comportamento quando o admin tenta rejeitar sem preencher o campo de motivo.
- **Resultado esperado:** Sistema impede a rejeição e apresenta mensagem de validação solicitando o motivo, mantendo a indicação na fila.
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 3 (a confirmar – validação de campo obrigatório)

### US08-CT06 — Indicação já com status “Ativo” não aparece na fila
- **Pré‑condição:** Admin autenticado; indicação previamente aprovada e com status **“Ativo”**.
- **Objetivo:** Garantir que indicações já processadas não são listadas como pendentes.
- **Resultado esperado:** Ao acessar a lista de indicadores pendentes, a indicação com status “Ativo” não é exibida.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT07 — Indicação já com status “Rejeitado” não aparece na fila
- **Pré‑condição:** Admin autenticado; indicação previamente rejeitada e com status **“Rejeitado”**.
- **Objetivo:** Verificar que indicações rejeitadas são removidas da lista de pendentes.
- **Resultado esperado:** A lista de pendentes não contém a indicação com status “Rejeitado”.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT08 — Falha de conexão ao atualizar status da indicação
- **Pré‑condição:** Admin autenticado; indicação com status “Pendente de aprovação”; banco de dados indisponível no momento da aprovação.
- **Objetivo:** Avaliar o tratamento de erro ao tentar mudar o status sem conexão ao DB.
- **Resultado esperado:** Sistema exibe mensagem de erro de persistência, mantém o status original da indicação (“Pendente de aprovação”) e a deixa visível na fila.
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 1/3 (a confirmar – tratamento de exceção)

### US08-CT09 — Usuário não‑admin tenta aprovar indicação
- **Pré‑condição:** Usuário autenticado sem permissão de admin; indicação com status “Pendente de aprovação”.
- **Objetivo:** Garantir que apenas admins podem aprovar ou rejeitar indicações.
- **Resultado esperado:** Sistema nega a ação, devolve código HTTP 403 (Forbidden) e mantém a indicação inalterada na fila.
- **Tipo:** alternativo
- **Critérios cobertos:** Todos os cenários (a confirmar – controle de acesso)