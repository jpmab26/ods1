### US01-CT01 — Cadastro de usuário com sucesso (Perfil Aluno)
- **Pré-condição:** Admin autenticado.
- **Objetivo:** Validar o cadastro de um novo usuário com perfil 'aluno'.
- **Resultado esperado:** Usuário é criado com status 'Pendente' e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastro de usuário com sucesso (Perfil Professor)
- **Pré-condição:** Admin autenticado.
- **Objetivo:** Validar o cadastro de um novo usuário com perfil 'professor'.
- **Resultado esperado:** Usuário é criado com status 'Pendente' e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastro de usuário com sucesso (Perfil Admin)
- **Pré-condição:** Admin autenticado.
- **Objetivo:** Validar o cadastro de um novo usuário com perfil 'admin'.
- **Resultado esperado:** Usuário é criado com status 'Pendente' e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT04 — Tentativa de cadastro com email já existente
- **Pré-condição:** Admin autenticado e usuário com o email a ser cadastrado já existe no sistema.
- **Objetivo:** Validar a rejeição do cadastro quando o email já está em uso.
- **Resultado esperado:** Sistema exibe a mensagem 'Email já cadastrado' e não cria o usuário.
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US01-CT05 — Cadastro com nome em branco
- **Pré-condição:** Admin autenticado.
- **Objetivo:** Validar o comportamento do sistema ao tentar cadastrar um usuário com o campo nome vazio.
- **Resultado esperado:** Critérios cobertos: a confirmar (O sistema deve apresentar uma mensagem de erro ou impedir o cadastro).
- **Tipo:** de validação
- **Critérios cobertos:** AC1

### US01-CT06 — Cadastro com email em branco
- **Pré-condição:** Admin autenticado.
- **Objetivo:** Validar o comportamento do sistema ao tentar cadastrar um usuário com o campo email vazio.
- **Resultado esperado:** Critérios cobertos: a confirmar (O sistema deve apresentar uma mensagem de erro ou impedir o cadastro).
- **Tipo:** de validação
- **Critérios cobertos:** AC1

### US01-CT07 — Cadastro com papel não selecionado
- **Pré-condição:** Admin autenticado.
- **Objetivo:** Validar o comportamento do sistema ao tentar cadastrar um usuário sem selecionar um papel.
- **Resultado esperado:** Critérios cobertos: a confirmar (O sistema deve apresentar uma mensagem de erro ou impedir o cadastro).
- **Tipo:** de validação
- **Critérios cobertos:** AC1

### US01-CT08 — Cadastro com nome muito longo
- **Pré-condição:** Admin autenticado.
- **Objetivo:** Validar o cadastro com um nome excedendo o limite esperado (se houver).
- **Resultado esperado:** Critérios cobertos: a confirmar (O sistema deve aceitar ou truncar/rejeitar o nome, com feedback apropriado).
- **Tipo:** de limite
- **Critérios cobertos:** AC1

### US01-CT09 — Cadastro com email inválido (formato)
- **Pré-condição:** Admin autenticado.
- **Objetivo:** Validar o cadastro com um endereço de email que não segue o formato padrão (ex: sem '@', sem domínio).
- **Resultado esperado:** Critérios cobertos: a confirmar (O sistema deve rejeitar o email inválido com uma mensagem de erro).
- **Tipo:** de validação
- **Critérios cobertos:** AC1

### US01-CT10 — Cadastro com nome contendo caracteres especiais
- **Pré-condição:** Admin autenticado.
- **Objetivo:** Validar o cadastro com um nome contendo caracteres especiais (ex: !, @, #, $).
- **Resultado esperado:** Critérios cobertos: a confirmar (O sistema deve aceitar ou rejeitar os caracteres especiais, dependendo das regras de negócio).
- **Tipo:** de validação
- **Critérios cobertos:** AC1