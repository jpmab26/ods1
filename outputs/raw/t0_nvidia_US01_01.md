### US01-CT01 — Cadastro de aluno com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel Aluno
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastro de professor com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel Professor (partição de equivalência de papel)
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastro de admin com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel Admin (partição de equivalência de papel)
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT04 — Cadastro com email já existente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; email já cadastrado na base
- **Objetivo:** Validar rejeição de email duplicado
- **Resultado esperado:** Sistema rejeita com mensagem 'Email já cadastrado'
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US01-CT05 — Cadastro com formato de email inválido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar tratamento de email com sintaxe inválida (partição de equivalência inválida)
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de erro de formato
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT06 — Cadastro com nome em branco
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar obrigatoriedade do campo nome (partição de equivalência vazia)
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de campo obrigatório
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT07 — Cadastro com email em branco
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar obrigatoriedade do campo email (partição de equivalência vazia)
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de campo obrigatório
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT08 — Cadastro sem selecionar papel
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar obrigatoriedade do campo papel (partição de equivalência vazia)
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de campo obrigatório
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT09 — Acesso à tela de cadastro sem autenticação
- **Pré-condição:** Usuário não autenticado tenta acessar URL da gestão de usuários
- **Objetivo:** Validar controle de acesso à funcionalidade
- **Resultado esperado:** Sistema redireciona para login ou exibe erro 403/401
- **Tipo:** segurança
- **Critérios cobertos:** a confirmar