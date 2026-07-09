### US08-CT01 — Aprovar indicação de monitor para disciplina sem monitor
- **Pré-condição:** Admin logado; existe uma indicação de monitor para uma disciplina sem monitor ativo, com status "Pendente de aprovação".
- **Objetivo:** Verificar a aprovação bem-sucedida de uma indicação para uma disciplina sem monitor.
- **Resultado esperado:** O status do vínculo muda para "Ativo" e o aluno associado passa a ter acesso como monitor da disciplina.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US08-CT02 — Aprovar alteração de monitor para disciplina com monitor existente (confirmando substituição)
- **Pré-condição:** Admin logado; existe uma indicação de alteração de monitor para uma disciplina que já possui um monitor ativo, com status "Pendente de aprovação de alteração de monitor".
- **Objetivo:** Verificar a aprovação bem-sucedida da alteração de monitor, substituindo o monitor antigo pelo novo.
- **Resultado esperado:** O sistema exibe uma pergunta de confirmação; após a confirmação, o status do vínculo muda para "Ativo", e apenas o aluno novo passa a ter acesso como monitor da disciplina (o monitor antigo é desativado para esta disciplina).
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2

### US08-CT03 — Aprovar alteração de monitor para disciplina com monitor existente (cancelando substituição)
- **Pré-condição:** Admin logado; existe uma indicação de alteração de monitor para uma disciplina que já possui um monitor ativo, com status "Pendente de aprovação de alteração de monitor".
- **Objetivo:** Verificar o comportamento ao cancelar a substituição do monitor antigo pelo novo na tela de confirmação.
- **Resultado esperado:** O sistema exibe uma pergunta de confirmação; após o cancelamento pelo admin, o status da indicação permanece "Pendente de aprovação de alteração de monitor", e o monitor antigo continua ativo.
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2 (a confirmar)

### US08-CT04 — Rejeitar indicação de monitor informando um motivo válido
- **Pré-condição:** Admin logado; existe uma indicação de monitor com status "Pendente de aprovação".
- **Objetivo:** Verificar a rejeição bem-sucedida de uma indicação, registrando o motivo fornecido.
- **Resultado esperado:** O status do vínculo muda para "Rejeitado" e o motivo informado pelo admin é salvo no sistema.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3

### US08-CT05 — Rejeitar indicação de monitor sem informar o motivo
- **Pré-condição:** Admin logado; existe uma indicação de monitor com status "Pendente de aprovação".
- **Objetivo:** Verificar se o sistema exige o preenchimento do motivo ao rejeitar uma indicação.
- **Resultado esperado:** O sistema impede a rejeição e exibe uma mensagem de erro/validação indicando que o motivo é obrigatório. O status da indicação permanece "Pendente de aprovação".
- **Tipo:** erro
- **Critérios cobertos:** Cenário 3 (a confirmar - obrigatoriedade do motivo não explícita na US, mas é uma variação relevante de entrada)

### US08-CT06 — Indicação aprovada não aparece mais na lista de pendentes
- **Pré-condição:** Admin logado; existe uma indicação de monitor com status "Pendente de aprovação" ou "Pendente de aprovação de alteração de monitor"; o admin aprovou esta indicação (conforme CT01 ou CT02).
- **Objetivo:** Verificar que uma indicação aprovada é removida da lista de indicações pendentes.
- **Resultado esperado:** Ao retornar à lista de indicações pendentes, a indicação que foi aprovada não é mais exibida.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4

### US08-CT07 — Indicação rejeitada não aparece mais na lista de pendentes
- **Pré-condição:** Admin logado; existe uma indicação de monitor com status "Pendente de aprovação"; o admin rejeitou esta indicação (conforme CT04).
- **Objetivo:** Verificar que uma indicação rejeitada é removida da lista de indicações pendentes.
- **Resultado esperado:** Ao retornar à lista de indicações pendentes, a indicação que foi rejeitada não é mais exibida.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4