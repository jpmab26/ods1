### US08-CT01 — Aprovar indicação de disciplina sem monitor (caminho feliz)
- **Pré‑condição:** Admin autenticado; disciplina sem monitor cadastrado; indicação em status “Pendente de aprovação”
- **Objetivo:** Verificar que a aprovação gera vínculo ativo e concede acesso ao novo monitor
- **Resultado esperado:** Sistema altera o status da indicação para “Ativo”, cria vínculo monitor‑disciplina, e o aluno passa a ter acesso ao módulo de monitoria da disciplina
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US08-CT02 — Aprovar indicação de disciplina com monitor (caminho feliz, confirmação aceita)
- **Pré‑condição:** Admin autenticado; disciplina já possui monitor ativo; indicação em status “Pendente de aprovação de alteração de monitor”
- **Objetivo:** Garantir que a aprovação substitui o monitor antigo pelo novo após confirmação
- **Resultado esperado:** Sistema exibe pergunta de confirmação; admin confirma; status da indicação muda para “Ativo”, vínculo do monitor antigo é encerrado e o novo monitor recebe vínculo ativo e acesso à disciplina
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2

### US08-CT03 — Aprovar indicação de disciplina com monitor (caminho alternativo, confirmação recusada)
- **Pré‑condição:** Admin autenticado; disciplina já possui monitor ativo; indicação em status “Pendente de aprovação de alteração de monitor”
- **Objetivo:** Verificar comportamento quando admin recusa a substituição
- **Resultado esperado:** Sistema exibe pergunta de confirmação; admin cancela; indicação permanece em “Pendente de aprovação de alteração de monitor” e nenhum vínculo é alterado
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2 (a confirmar)

### US08-CT04 — Rejeitar indicação informando motivo
- **Pré‑condição:** Admin autenticado; indicação em status “Pendente de aprovação”
- **Objetivo:** Confirmar que a rejeição registra o motivo e muda o status para “Rejeitado”
- **Resultado esperado:** Sistema altera status da indicação para “Rejeitado”, grava o motivo informado e não cria vínculo monitor‑disciplina
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3

### US08-CT05 — Rejeitar indicação sem informar motivo (campo obrigatório não preenchido)
- **Pré‑condição:** Admin autenticado; indicação em status “Pendente de aprovação”
- **Objetivo:** Verificar validação de preenchimento do motivo ao rejeitar
- **Resultado esperado:** Sistema impede o envio, exibe mensagem de erro “Motivo é obrigatório”, a indicação permanece em “Pendente de aprovação”
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 3 (a confirmar)

### US08-CT06 — Indicação aprovada desaparece da lista de pendentes
- **Pré‑condição:** Admin autenticado; indicação pendente já aprovada (status agora “Ativo”)
- **Objetivo:** Garantir que a lista de indicações pendentes não exibe itens já processados
- **Resultado esperado:** Ao retornar à tela de lista de pendentes, a indicação aprovada não aparece mais
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT07 — Indicação rejeitada desaparece da lista de pendentes
- **Pré‑condição:** Admin autenticado; indicação pendente já rejeitada (status “Rejeitado”)
- **Objetivo:** Garantir que a lista de indicações pendentes não exibe itens já processados
- **Resultado esperado:** Ao retornar à tela de lista de pendentes, a indicação rejeitada não aparece mais
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT08 — Tentativa de aprovação por usuário não‑admin
- **Pré‑condição:** Usuário autenticado com perfil diferente de admin; indicação em status “Pendente de aprovação”
- **Objetivo:** Verificar controle de acesso à funcionalidade de aprovação
- **Resultado esperado:** Sistema impede a ação, exibe mensagem “Acesso negado”, a indicação permanece inalterada
- **Tipo:** segurança
- **Critérios cobertos:** AC geral (a confirmar)

### US08-CT09 — Aprovação quando a indicação já está em status “Ativo”
- **Pré‑condição:** Admin autenticado; indicação previamente aprovada (status “Ativo”)
- **Objetivo:** Testar idempotência da operação de aprovação
- **Resultado esperado:** Sistema informa “Indicação já aprovada”, nenhum efeito colateral ocorre; a indicação continua “Ativo”
- **Tipo:** alternativo
- **Critérios cobertos:** AC geral (a confirmar)

### US08-CT10 — Rejeição quando a indicação já está em status “Rejeitado”
- **Pré‑condição:** Admin autenticado; indicação previamente rejeitada (status “Rejeitado”) com motivo registrado
- **Objetivo:** Testar idempotência da operação de rejeição
- **Resultado esperado:** Sistema informa “Indicação já rejeitada”, nenhum novo motivo é registrado; o status permanece “Rejeitado”
- **Tipo:** alternativo
- **Critérios cobertos:** AC geral (a confirmar)