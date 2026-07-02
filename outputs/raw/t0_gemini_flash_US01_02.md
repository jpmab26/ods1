### US01-CT01 — Cadastrar usuário com perfil 'aluno'
- **Pré-condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro bem-sucedido de um novo usuário com o perfil 'aluno'.
- **Resultado esperado:** O sistema cria um novo usuário com o perfil 'aluno', status 'Pendente', e exibe uma senha temporária ao admin.
- **Tipo:** principal
- **Critérios cobertos:** BDD 1

### US01-CT02 — Cadastrar usuário com perfil 'professor'
- **Pré-condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro bem-sucedido de um novo usuário com o perfil 'professor'.
- **Resultado esperado:** O sistema cria um novo usuário com o perfil 'professor', status 'Pendente', e exibe uma senha temporária ao admin.
- **Tipo:** principal
- **Critérios cobertos:** BDD 1

### US01-CT03 — Cadastrar usuário com perfil 'admin'
- **Pré-condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro bem-sucedido de um novo usuário com o perfil 'admin'.
- **Resultado esperado:** O sistema cria um novo usuário com o perfil 'admin', status 'Pendente', e exibe uma senha temporária ao admin.
- **Tipo:** principal
- **Critérios cobertos:** BDD 1

### US01-CT04 — Tentar cadastrar usuário com email já existente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; Um usuário com o email informado já existe no sistema.
- **Objetivo:** Validar que o sistema rejeita o cadastro de um usuário com um email já existente.
- **Resultado esperado:** O sistema exibe a mensagem 'Email já cadastrado' e o novo usuário não é criado.
- **Tipo:** alternativo/negativo
- **Critérios cobertos:** BDD 2