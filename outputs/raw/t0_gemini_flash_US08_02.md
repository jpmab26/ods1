### US08-CT01 — Aprovar indicação de monitor para disciplina sem monitor prévio
- **Pré-condição:** Admin logado. Existe uma indicação de monitor com status "Pendente de aprovação" para uma disciplina que *não* possui um monitor ativo.
- **Objetivo:** Verificar a aprovação bem-sucedida de uma indicação de monitor para uma disciplina sem monitor prévio.
- **Resultado esperado:** O status do vínculo da indicação muda para "Ativo". O aluno indicado obtém acesso e funcionalidades de monitor para a disciplina. A indicação processada não aparece mais na lista de pendentes de aprovação.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1, Cenário 4

### US08-CT02 — Aprovar alteração de monitor (confirmando substituição)
- **Pré-condição:** Admin logado. Existe uma indicação de monitor com status "Pendente de aprovação de alteração de monitor" para uma disciplina que *já* possui um monitor ativo.
- **Objetivo:** Verificar a aprovação bem-sucedida de uma alteração de monitor, confirmando a substituição do monitor antigo pelo novo.
- **Resultado esperado:** O sistema solicita confirmação para a alteração do monitor. Após aceitar a confirmação, o status do vínculo do *novo* monitor muda para "Ativo". O vínculo do *monitor antigo* para esta disciplina é desativado ou tem seu status alterado para indicar inatividade/substituição. Apenas o aluno novo tem acesso e funcionalidades de monitor para a disciplina. A indicação processada não aparece mais na lista de pendentes de aprovação.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2, Cenário 4

### US08-CT03 — Aprovar alteração de monitor (cancelando substituição)
- **Pré-condição:** Admin logado. Existe uma indicação de monitor com status "Pendente de aprovação de alteração de monitor" para uma disciplina que *já* possui um monitor ativo.
- **Objetivo:** Verificar o comportamento do sistema ao aprovar uma alteração de monitor, mas cancelar a confirmação da substituição.
- **Resultado esperado:** O sistema solicita confirmação para a alteração do monitor. Após *cancelar* a confirmação, o status do vínculo do novo monitor e do monitor antigo *não* são alterados. A indicação *permanece* com o status "Pendente de aprovação de alteração de monitor" e *ainda aparece* na lista de pendentes.
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2 (a confirmar)

### US08-CT04 — Rejeitar indicação de monitor com motivo válido
- **Pré-condição:** Admin logado. Existe uma indicação de monitor com status "Pendente de aprovação".
- **Objetivo:** Verificar a rejeição bem-sucedida de uma indicação de monitor, informando um motivo válido.
- **Resultado esperado:** O sistema solicita um motivo para a rejeição. Após informar um motivo e confirmar a rejeição, o status do vínculo da indicação muda para "Rejeitado". O motivo informado é registrado e associado à indicação. A indicação processada não aparece mais na lista de pendentes de aprovação.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3, Cenário 4

### US08-CT05 — Rejeitar indicação de monitor sem motivo
- **Pré-condição:** Admin logado. Existe uma indicação de monitor com status "Pendente de aprovação".
- **Objetivo:** Verificar o comportamento do sistema ao tentar rejeitar uma indicação sem informar o motivo.
- **Resultado esperado:** O sistema exibe uma mensagem de erro ou validação indicando que o motivo é obrigatório. O status do vínculo da indicação *não* é alterado e permanece "Pendente de aprovação". A indicação *ainda aparece* na lista de pendentes.
- **Tipo:** erro/validação
- **Critérios cobertos:** Cenário 3 (a confirmar obrigatoriedade do motivo)