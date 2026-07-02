### US01-CT01 — Cadastro de novo usuário com perfil Aluno
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro de um novo usuário com o perfil "aluno".
- **Resultado esperado:** O usuário é criado com o status "Pendente", e uma senha temporária é exibida para o admin. O usuário "aluno" é listado na tela de gestão de usuários.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastro de novo usuário com perfil Professor
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro de um novo usuário com o perfil "professor".
- **Resultado esperado:** O usuário é criado com o status "Pendente", e uma senha temporária é exibida para o admin. O usuário "professor" é listado na tela de gestão de usuários.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastro de novo usuário com perfil Admin
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro de um novo usuário com o perfil "admin".
- **Resultado esperado:** O usuário é criado com o status "Pendente", e uma senha temporária é exibida para o admin. O usuário "admin" é listado na tela de gestão de usuários.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT04 — Tentar cadastrar email já existente
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários. Um usuário com o email "teste@exemplo.com" já existe no sistema.
- **Objetivo:** Validar a rejeição do cadastro quando o email já está em uso.
- **Resultado esperado:** O sistema exibe a mensagem de erro "Email já cadastrado" e não cria o novo usuário.
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US01-CT05 — Cadastro com campo Nome vazio
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários.
- **Objetivo:** Validar o comportamento do sistema ao tentar cadastrar um usuário com o campo "Nome" vazio.
- **Resultado esperado:** O cadastro é rejeitado. O sistema deve exibir uma mensagem de validação informando que o campo nome é obrigatório (a mensagem exata deve ser confirmada com a equipe).
- **Tipo:** validação
- **Critérios cobertos:** AC1 (a confirmar)

### US01-CT06 — Cadastro com campo Email vazio
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários.
- **Objetivo:** Validar o comportamento do sistema ao tentar cadastrar um usuário com o campo "Email" vazio.
- **Resultado esperado:** O cadastro é rejeitado. O sistema deve exibir uma mensagem de validação informando que o campo email é obrigatório (a mensagem exata deve ser confirmada com a equipe).
- **Tipo:** validação
- **Critérios cobertos:** AC1 (a confirmar)

### US01-CT07 — Cadastro com campo Papel não selecionado
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários.
- **Objetivo:** Validar o comportamento do sistema ao tentar cadastrar um usuário sem selecionar um "Papel".
- **Resultado esperado:** O cadastro é rejeitado. O sistema deve exibir uma mensagem de validação informando que o papel é obrigatório (a mensagem exata deve ser confirmada com a equipe).
- **Tipo:** validação
- **Critérios cobertos:** AC1 (a confirmar)

### US01-CT08 — Cadastro com email em formato inválido
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro com um email em formato inválido (ex: "emailinvalido.com").
- **Resultado esperado:** O cadastro é rejeitado. O sistema deve exibir uma mensagem de validação informando que o formato do email é inválido (a mensagem exata deve ser confirmada com a equipe).
- **Tipo:** validação
- **Critérios cobertos:** AC1 (a confirmar)

### US01-CT09 — Cadastro com email contendo caracteres especiais não permitidos
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários.
- **Objetivo:** Validar o cadastro com um email contendo caracteres especiais não permitidos (ex: "email com espaço@exemplo.com").
- **Resultado esperado:** O cadastro é rejeitado. O sistema deve exibir uma mensagem de validação informando que o email contém caracteres inválidos (a mensagem exata deve ser confirmada com a equipe).
- **Tipo:** validação
- **Critérios cobertos:** AC1 (a confirmar)

### US01-CT10 — Verificação do status "Pendente" após cadastro
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários. Um usuário foi cadastrado recentemente.
- **Objetivo:** Verificar se o usuário recém-cadastrado possui o status "Pendente".
- **Resultado esperado:** O usuário listado na tela de gestão de usuários apresenta o status "Pendente".
- **Tipo:** validação
- **Critérios cobertos:** AC1

### US01-CT11 — Verificação da exibição da senha temporária ao admin
- **Pré-condição:** Admin autenticado no sistema, na tela de gestão de usuários. Um usuário foi cadastrado recentemente.
- **Objetivo:** Verificar se uma senha temporária é exibida para o admin após o cadastro.
- **Resultado esperado:** Uma senha temporária é exibida claramente na interface para o admin após a confirmação do cadastro.
- **Tipo:** validação
- **Critérios cobertos:** AC1