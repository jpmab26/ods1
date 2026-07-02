### US08-CT01 — Aprovação de indicação de monitor sem pré-existente
- **Pré-condição:** Admin logado. Existe uma indicação de monitor para uma disciplina que *não possui monitor atualmente*, com status "Pendente de aprovação".
- **Objetivo:** Aprovar uma indicação de monitor para uma disciplina sem monitor pré-existente.
- **Resultado esperado:** O status do vínculo da indicação muda para "Ativo". O aluno indicado passa a ter acesso como monitor da disciplina no sistema.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US08-CT02 — Aprovação de alteração de monitor com confirmação
- **Pré-condição:** Admin logado. Existe uma indicação de alteração de monitor para uma disciplina que *já possui monitor*, com status "Pendente de aprovação de alteração de monitor".
- **Objetivo:** Aprovar a alteração de monitor, confirmando a substituição do monitor antigo pelo novo.
- **Resultado esperado:** O sistema exibe uma caixa de diálogo para confirmar a alteração do monitor antigo pelo novo. Após a confirmação, o status do vínculo do aluno novo muda para "Ativo". O aluno novo passa a ter acesso como monitor da disciplina, e o aluno antigo perde esse acesso.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2

### US08-CT03 — Rejeição de indicação com motivo
- **Pré-condição:** Admin logado. Existe uma indicação de monitor (seja "Pendente de aprovação" ou "Pendente de aprovação de alteração de monitor" – o Cenário 3 especifica "Pendente de aprovação", então usaremos essa) com status "Pendente de aprovação".
- **Objetivo:** Rejeitar uma indicação de monitor, fornecendo um motivo.
- **Resultado esperado:** O status do vínculo da indicação muda para "Rejeitado". O motivo informado é registrado e associado à indicação.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3

### US08-CT04 — Indicação "Pendente de aprovação" não visível na lista após aprovação
- **Pré-condição:** Admin logado. Uma indicação de monitor com status "Pendente de aprovação" foi aprovada (conforme US08-CT01).
- **Objetivo:** Verificar se uma indicação processada por aprovação é removida da lista de pendentes.
- **Resultado esperado:** Ao retornar para a lista de indicações pendentes de aprovação, a indicação que foi processada (aprovada) não aparece mais na lista.
- **Tipo:** fluxo alternativo
- **Critérios cobertos:** Cenário 4

### US08-CT05 — Indicação "Pendente de aprovação de alteração" não visível na lista após aprovação
- **Pré-condição:** Admin logado. Uma indicação de alteração de monitor com status "Pendente de aprovação de alteração de monitor" foi aprovada (conforme US08-CT02).
- **Objetivo:** Verificar se uma indicação de alteração processada por aprovação é removida da lista de pendentes.
- **Resultado esperado:** Ao retornar para a lista de indicações pendentes, a indicação de alteração que foi processada (aprovada) não aparece mais na lista.
- **Tipo:** fluxo alternativo
- **Critérios cobertos:** Cenário 4

### US08-CT06 — Indicação "Pendente de aprovação" não visível na lista após rejeição
- **Pré-condição:** Admin logado. Uma indicação de monitor com status "Pendente de aprovação" foi rejeitada (conforme US08-CT03).
- **Objetivo:** Verificar se uma indicação processada por rejeição é removida da lista de pendentes.
- **Resultado esperado:** Ao retornar para a lista de indicações pendentes de aprovação, a indicação que foi processada (rejeitada) não aparece mais na lista.
- **Tipo:** fluxo alternativo
- **Critérios cobertos:** Cenário 4