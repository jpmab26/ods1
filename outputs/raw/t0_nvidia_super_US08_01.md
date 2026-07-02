### US08-CT01 — Aprovação de indicação para disciplina sem monitor
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação" vinculada a uma disciplina que atualmente não possui monitor atribuído; o admin está autenticado e na tela de lista de pendências.
- **Objetivo:** Verificar que ao aprovar a indicação o vínculo passa para "Ativo" e o aluno ganha acesso como monitor da disciplina.
- **Resultado esperado:** Sistema atualiza o status da indicação para "Ativo", registra o aluno como monitor da disciplina e exibe mensagem de sucesso.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US08-CT02 — Aprovação de indicação para disciplina com monitor existente, confirmando substituição
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação de alteração de monitor" para uma disciplina que já possui um monitor ativo; o admin está autenticado e visualiza a indicação.
- **Objetivo:** Validar que, ao aprovar a alteração e confirmar a substituição, o monitor antigo é substituído pelo novo e o vínculo fica "Ativo".
- **Resultado esperado:** Sistema solicita confirmação de substituição; após confirmação, atualiza o status da indicação para "Ativo", remove o acesso do monitor antigo e atribui o novo aluno como monitor da disciplina.
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US08-CT03 — Aprovação de indicação para disciplina com monitor existente, cancelando substituição
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação de alteração de monitor" para disciplina com monitor ativo; admin na tela da indicação.
- **Objetivo:** Verificar que, ao iniciar a aprovação e cancelar a confirmação de substituição, nenhuma alteração ocorre.
- **Resultado esperado:** Sistema apresenta a tela de confirmação; ao selecionar "Cancelar", mantém o status da indicação como "Pendente de aprovação de alteração de monitor" e preserva o monitor atual.
- **Tipo:** alternativo
- **Critérios cobertos:** AC2 (comportamento de cancelamento a confirmar)

### US08-CT04 — Rejeição de indicação com motivo informado
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação"; admin autenticado e na tela da indicação.
- **Objetivo:** Confirmar que ao rejeitar indicando motivo, o status passa para "Rejeitado" e o motivo é registrado.
- **Resultado esperado:** Sistema salva o motivo fornecido, atualiza o status da indicação para "Rejeitado" e exibe mensagem de confirmação.
- **Tipo:** principal
- **Critérios cobertos:** AC3

### US08-CT05 — Tentativa de rejeição de indicação sem informar motivo
- **Pré-condição:** Existe uma indicação de monitor com status "Pendente de aprovação"; admin na tela de rejeição.
- **Objetivo:** Verificar comportamento do sistema quando o motivo não é preenchido (regra não especificada na user story).
- **Resultado esperado:** Sistema impede a rejeição e solicita que o motivo seja informado (ou exibe mensagem de validação). Como a regra não está descrita, o resultado é a confirmar.
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar

### US08-CT06 — Indicação processada (aprovada ou rejeitada) não aparece mais na lista de pendências
- **Pré-condição:** Existe pelo menos uma indicação com status "Pendente de aprovação" na lista; admin autenticado.
- **Objetivo:** Assegurar que após aprovar ou rejeitar a indicação, ela some da lista de pendências.
- **Resultado esperado:** Ao retornar à lista de pendências, a indicação processada não está mais presente; apenas as demais pendências permanecem.
- **Tipo:** principal
- **Critérios cobertos:** AC4

### US08-CT07 — Tentativa de aprovar indicação já processada (status diferente de pendente)
- **Pré-condição:** Existe uma indicação com status "Ativo" ou "Rejeitado"; admin tenta acessar a ação de aprovação.
- **Objetivo:** Verificar que o sistema não permite aprovação de indicação não pendente.
- **Resultado esperado:** Sistema desativa o botão/ link de aprovação ou exibe mensagem de erro indicando que a indicação já foi processada.
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar

### US08-CT08 — Tentativa de rejeitar indicação já processada (status diferente de pendente)
- **Pré-condição:** Existe uma indicação com status "Ativo" ou "Rejeitado"; admin tenta acessar a ação de rejeição.
- **Objetivo:** Verificar que o sistema não permite rejeição de indicação não pendente.
- **Resultado esperado:** Sistema desativa o botão/ link de rejeição ou exibe mensagem de erro indicando que a indicação já foi processada.
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar