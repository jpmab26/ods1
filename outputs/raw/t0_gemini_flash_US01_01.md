### US01-CT01 — Admin cadastra usuário com perfil 'Aluno'
- **Pré-condição:** Admin autenticado na tela de gestão de usuários. Não há usuário com o email 'aluno.novo@dominio.com' no sistema.
- **Objetivo:** Validar o cadastro bem-sucedido de um novo usuário com o perfil 'Aluno'.
- **Resultado esperado:** Usuário é criado com nome 'Aluno Teste', email 'aluno.novo@dominio.com', perfil 'Aluno' e status 'Pendente'. Uma senha temporária é exibida ao admin.
- **Tipo:** Principal
- **Critérios cobertos:** BDD1

### US01-CT02 — Admin cadastra usuário com perfil 'Professor'
- **Pré-condição:** Admin autenticado na tela de gestão de usuários. Não há usuário com o email 'professor.novo@dominio.com' no sistema.
- **Objetivo:** Validar o cadastro bem-sucedido de um novo usuário com o perfil 'Professor'.
- **Resultado esperado:** Usuário é criado com nome 'Professor Teste', email 'professor.novo@dominio.com', perfil 'Professor' e status 'Pendente'. Uma senha temporária é exibida ao admin.
- **Tipo:** Principal
- **Critérios cobertos:** BDD1

### US01-CT03 — Admin cadastra usuário com perfil 'Admin'
- **Pré-condição:** Admin autenticado na tela de gestão de usuários. Não há usuário com o email 'admin.novo@dominio.com' no sistema.
- **Objetivo:** Validar o cadastro bem-sucedido de um novo usuário com o perfil 'Admin'.
- **Resultado esperado:** Usuário é criado com nome 'Admin Teste', email 'admin.novo@dominio.com', perfil 'Admin' e status 'Pendente'. Uma senha temporária é exibida ao admin.
- **Tipo:** Principal
- **Critérios cobertos:** BDD1

### US01-CT04 — Admin tenta cadastrar usuário com email já existente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários. Já existe um usuário com o email 'existente@dominio.com' no sistema.
- **Objetivo:** Validar que o sistema rejeita o cadastro de um usuário com um email já em uso.
- **Resultado esperado:** O sistema exibe a mensagem 'Email já cadastrado'. Nenhum novo usuário é criado.
- **Tipo:** Erro
- **Critérios cobertos:** BDD2