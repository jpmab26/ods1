### US07-CT01 — Professor indica aluno válido como monitor
- **Pré-condição:** Professor autenticado e acessando a tela de uma disciplina sob sua responsabilidade. Existe um aluno cadastrado, ativo, com papel "aluno", e que ainda não é monitor daquela disciplina específica.
- **Objetivo:** Validar a criação de um vínculo de monitoria para um aluno válido.
- **Resultado esperado:** O sistema cria um vínculo de monitoria entre a disciplina e o aluno, com o status "Pendente de aprovação".
- **Tipo:** Principal
- **Critérios cobertos:** Cenário 1

### US07-CT02 — Professor tenta indicar usuário com papel "Professor"
- **Pré-condição:** Professor autenticado e acessando a tela de uma disciplina sob sua responsabilidade. Existe um usuário cadastrado e ativo com o papel "Professor".
- **Objetivo:** Validar que o sistema rejeita a indicação de um usuário com papel "Professor".
- **Resultado esperado:** O sistema exibe uma mensagem de erro indicando que o papel do usuário é inválido para ser monitor (ex: "Usuário não possui papel de aluno para ser indicado como monitor.").
- **Tipo:** Exceção/Erro
- **Critérios cobertos:** Cenário 2

### US07-CT03 — Professor tenta indicar usuário sem papel "aluno" (ex: Administrador)
- **Pré-condição:** Professor autenticado e acessando a tela de uma disciplina sob sua responsabilidade. Existe um usuário cadastrado e ativo com um papel diferente de "aluno" ou "professor" (e.g., "Administrador" ou nenhum papel específico de monitoria/disciplina).
- **Objetivo:** Validar que o sistema rejeita a indicação de um usuário sem o papel "aluno".
- **Resultado esperado:** O sistema exibe uma mensagem de erro indicando que o papel do usuário é inválido para ser monitor (ex: "Usuário não possui papel de aluno para ser indicado como monitor.").
- **Tipo:** Exceção/Erro
- **Critérios cobertos:** Cenário 2

### US07-CT04 — Professor não visualiza disciplina de outro professor para indicação
- **Pré-condição:** Professor autenticado. Existem múltiplas disciplinas cadastradas no sistema, algumas sob a responsabilidade do professor autenticado e outras sob a responsabilidade de outros professores.
- **Objetivo:** Validar que o professor só pode indicar monitores para suas próprias disciplinas.
- **Resultado esperado:** Ao listar as disciplinas para indicação de monitor (ou ao navegar pelas opções de disciplinas), o professor visualiza e tem acesso somente às disciplinas pelas quais é responsável. Disciplinas de outros professores não aparecem como opção selecionável para indicação de monitor.
- **Tipo:** Validação de acesso/interface
- **Critérios cobertos:** Cenário 3