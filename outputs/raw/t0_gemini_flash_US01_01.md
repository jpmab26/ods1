### US01-CT01 — Cadastrar usuário com perfil 'aluno'
- **Pré-condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro bem-sucedido de um novo usuário com o perfil 'aluno'.
- **Resultado esperado:** Um novo usuário com perfil 'aluno' é criado, seu status é 'Pendente', e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastrar usuário com perfil 'professor'
- **Pré-condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro bem-sucedido de um novo usuário com o perfil 'professor'.
- **Resultado esperado:** Um novo usuário com perfil 'professor' é criado, seu status é 'Pendente', e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastrar usuário com perfil 'admin'
- **Pré-condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro bem-sucedido de um novo usuário com o perfil 'admin'.
- **Resultado esperado:** Um novo usuário com perfil 'admin' é criado, seu status é 'Pendente', e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT04 — Tentar cadastrar usuário com email já existente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários. Existe um usuário previamente cadastrado no sistema com o email informado para o novo cadastro.
- **Objetivo:** Validar que o sistema impede o cadastro de um usuário com um email que já está em uso.
- **Resultado esperado:** O sistema rejeita o cadastro e exibe a mensagem 'Email já cadastrado'.
- **Tipo:** alternativo/erro
- **Critérios cobertos:** AC2