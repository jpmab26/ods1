### US07-CT01 — Indicação bem-sucedida
- **Pré-condição:** Professor autenticado na tela de uma disciplina que leciona; existe pelo menos um aluno cadastrado com papel "aluno" no sistema.
- **Objetivo:** Validar que a indicação de um aluno como monitor cria vínculo com status "Pendente de aprovação".
- **Resultado esperado:** Após selecionar o aluno e confirmar a indicação, o sistema exibe mensagem de sucesso e o vínculo aparece na lista de monitores da disciplina com status "Pendente de aprovação".
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US07-CT02 — Indicação de usuário não aluno
- **Pré-condição:** Professor autenticado na tela de uma disciplina que leciona; existe usuário cadastrado sem papel "aluno" (ex: coordenador, outro professor).
- **Objetivo:** Verificar que o sistema rejeita a indicação de usuário que não possui papel "aluno".
- **Resultado esperado:** Ao confirmar a indicação, o sistema exibe mensagem de erro indicando papel inválido e não cria nenhum vínculo.
- **Tipo:** alternativa
- **Critérios cobertos:** AC2

### US07-CT03 — Indicação de aluno já monitor da mesma disciplina
- **Pré-condição:** Professor autenticado na tela de uma disciplina que leciona; existe aluno já vinculado como monitor da mesma disciplina (qualquer status).
- **Objetivo:** Verificar comportamento ao indicar novamente o mesmo aluno como monitor, já monitor, já que a regra não está especificada na user story.
- **Resultado esperado:** O sistema pode impedir a duplicação ou permitir nova indicação; como não há regra definida, o resultado deve ser observado e a aceitação marcada a confirmar.
- **Tipo:** alternativa
- **Critérios cobertos:** a confirmar

### US07-CT04 — Disciplina de outro professor não aparece nas opções
- **Pré-condição:** Professor autenticado; tenta acessar a lista de disciplinas para indicar monitor, estando visualizando tela de disciplina que NÃO leciona (disciplina de outro professor).
- **Objetivo:** Garantir que disciplinas das quais o professor não é responsável não sejam apresentadas como opções para indicação.
- **Resultado esperado:** A lista de disciplinas exibe apenas aquelas das quais o professor é responsável; a disciplina de outro professor está ausente das opções.
- **Tipo:** alternativa
- **Critérios cobertos:** AC3