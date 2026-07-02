### US08-CT01 — Aprovar indicação de monitor para disciplina sem monitor prévio
- **Pré-condição:** Admin logado. Existe uma indicação de monitor para uma disciplina sem monitor ativo com status "Pendente de aprovação".
- **Objetivo:** Aprovar uma indicação de monitor para uma disciplina que não possui monitor ativo.
- **Resultado esperado:** O vínculo do aluno com a disciplina muda para "Ativo". O aluno indicado passa a ter acesso como monitor da disciplina.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US08-CT02 — Aprovar alteração de monitor para disciplina com monitor prévio (confirmando)
- **Pré-condição:** Admin logado. Existe uma indicação de alteração de monitor para uma disciplina que já possui monitor ativo, com status "Pendente de aprovação de alteração de monitor".
- **Objetivo:** Aprovar uma alteração de monitor para uma disciplina que já possui monitor ativo, aceitando a confirmação da substituição.
- **Resultado esperado:** O sistema solicita confirmação da alteração do monitor antigo pelo novo. Após aceita, o vínculo do aluno novo muda para "Ativo" e apenas ele passa a ter acesso como monitor da disciplina. O monitor antigo é desativado ou tem seu acesso removido.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2

### US08-CT03 — Rejeitar indicação de monitor com motivo
- **Pré-condição:** Admin logado. Existe uma indicação de monitor para uma disciplina com status "Pendente de aprovação" (ou "Pendente de aprovação de alteração de monitor").
- **Objetivo:** Rejeitar uma indicação de monitor informando um motivo válido.
- **Resultado esperado:** O vínculo do aluno com a disciplina muda para "Rejeitado" e o motivo informado é registrado.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3

### US08-CT04 — Indicação aprovada não aparece mais na lista de pendentes
- **Pré-condição:** Admin logado. Uma indicação foi aprovada (cenários US08-CT01 ou US08-CT02 foram executados com sucesso).
- **Objetivo:** Verificar que uma indicação aprovada não é mais exibida na lista de indicações pendentes.
- **Resultado esperado:** Ao retornar à lista de indicações pendentes, a indicação que foi processada (aprovada) não aparece mais.
- **Tipo:** principal (follow-up)
- **Critérios cobertos:** Cenário 4

### US08-CT05 — Indicação rejeitada não aparece mais na lista de pendentes
- **Pré-condição:** Admin logado. Uma indicação foi rejeitada (cenário US08-CT03 foi executado com sucesso).
- **Objetivo:** Verificar que uma indicação rejeitada não é mais exibida na lista de indicações pendentes.
- **Resultado esperado:** Ao retornar à lista de indicações pendentes, a indicação que foi processada (rejeitada) não aparece mais.
- **Tipo:** principal (follow-up)
- **Critérios cobertos:** Cenário 4

### US08-CT06 — Tentar rejeitar indicação sem informar o motivo
- **Pré-condição:** Admin logado. Existe uma indicação de monitor com status "Pendente de aprovação" (ou "Pendente de aprovação de alteração de monitor").
- **Objetivo:** Tentar rejeitar uma indicação de monitor sem fornecer um motivo.
- **Resultado esperado:** O sistema impede a rejeição e/ou exibe uma mensagem de erro informando que o motivo é obrigatório. O status do vínculo permanece inalterado.
- **Tipo:** negativo
- **Critérios cobertos:** Cenário 3 (a confirmar se o motivo é obrigatório para rejeição)

### US08-CT07 — Tentar aprovar alteração de monitor mas não confirmar a substituição
- **Pré-condição:** Admin logado. Existe uma indicação de alteração de monitor para uma disciplina que já possui monitor ativo, com status "Pendente de aprovação de alteração de monitor".
- **Objetivo:** Iniciar o processo de aprovação de alteração de monitor, mas cancelar ou não aceitar a etapa de confirmação da substituição.
- **Resultado esperado:** O vínculo do aluno indicado permanece com o status "Pendente de aprovação de alteração de monitor". O monitor antigo continua ativo.
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2 (a confirmar comportamento em caso de não aceitação da confirmação)