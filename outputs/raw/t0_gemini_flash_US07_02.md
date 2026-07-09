### US07-CT01 — Indicação bem-sucedida de aluno como monitor
- **Pré-condição:** Professor autenticado na tela de uma de suas disciplinas. Existe um aluno válido cadastrado no sistema.
- **Objetivo:** Validar a criação de vínculo de monitoria com status "Pendente de aprovação" após indicação.
- **Resultado esperado:** Vínculo de monitoria é criado para o aluno na disciplina, com status "Pendente de aprovação".
- **Tipo:** Principal
- **Critérios cobertos:** Cenário 1

### US07-CT02 — Indicação de usuário com papel de professor (não aluno)
- **Pré-condição:** Professor autenticado na tela de uma de suas disciplinas. Existe um usuário cadastrado com papel "professor" (e sem papel "aluno").
- **Objetivo:** Validar que o sistema rejeita a indicação de um usuário que não possui o papel "aluno".
- **Resultado esperado:** Sistema exibe uma mensagem de erro indicando que o papel do usuário é inválido para indicação como monitor.
- **Tipo:** Exceção
- **Critérios cobertos:** Cenário 2

### US07-CT03 — Indicação de usuário sem papel de aluno (sem papel específico)
- **Pré-condição:** Professor autenticado na tela de uma de suas disciplinas. Existe um usuário cadastrado sem o papel "aluno" (e sem outro papel específico como "professor" ou "admin").
- **Objetivo:** Validar que o sistema rejeita a indicação de um usuário que não possui o papel "aluno".
- **Resultado esperado:** Sistema exibe uma mensagem de erro indicando que o papel do usuário é inválido para indicação como monitor.
- **Tipo:** Exceção
- **Critérios cobertos:** Cenário 2

### US07-CT04 — Disciplina de outro professor não aparece nas opções de indicação
- **Pré-condição:** Professor autenticado. Existe uma disciplina cadastrada que não é de responsabilidade do professor autenticado.
- **Objetivo:** Validar que o professor não consegue visualizar ou selecionar disciplinas que não são de sua responsabilidade para indicação de monitor.
- **Resultado esperado:** A disciplina que não é de responsabilidade do professor não aparece nas opções disponíveis para ele.
- **Tipo:** Exceção
- **Critérios cobertos:** Cenário 3

### US07-CT05 — Professor visualiza apenas suas disciplinas para indicação
- **Pré-condição:** Professor autenticado. Existem múltiplas disciplinas cadastradas, algumas de responsabilidade do professor e outras não.
- **Objetivo:** Validar que a tela de indicação de monitor exibe somente as disciplinas pelas quais o professor autenticado é responsável.
- **Resultado esperado:** Somente as disciplinas pelas quais o professor é responsável são exibidas nas opções disponíveis para indicação de monitor.
- **Tipo:** Principal
- **Critérios cobertos:** Cenário 3 (aspecto positivo)