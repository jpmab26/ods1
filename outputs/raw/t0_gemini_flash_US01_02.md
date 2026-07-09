### US01-CT01 — Admin cadastra usuário Aluno
- **Pré-condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro de um novo usuário com perfil 'Aluno'.
- **Resultado esperado:** Usuário 'Aluno' é criado com status 'Pendente' e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** BDD 1

### US01-CT02 — Admin cadastra usuário Professor
- **Pré-condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro de um novo usuário com perfil 'Professor'.
- **Resultado esperado:** Usuário 'Professor' é criado com status 'Pendente' e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** BDD 1

### US01-CT03 — Admin cadastra usuário Admin
- **Pré-condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro de um novo usuário com perfil 'Admin'.
- **Resultado esperado:** Usuário 'Admin' é criado com status 'Pendente' e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** BDD 1

### US01-CT04 — Admin tenta cadastrar email já existente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; Um usuário com um email específico já existe no sistema.
- **Objetivo:** Validar que o sistema rejeita o cadastro de um usuário com um email já existente.
- **Resultado esperado:** Sistema rejeita o cadastro e exibe a mensagem 'Email já cadastrado'.
- **Tipo:** exceção
- **Critérios cobertos:** BDD 2