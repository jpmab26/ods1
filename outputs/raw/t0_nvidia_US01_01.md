### US01-CT01 — Cadastro de aluno com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel Aluno
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastro de professor com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel Professor
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastro de admin com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel Admin
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT04 — Cadastro com email já existente
- **Pré-condição:** Admin autenticado; email "joao@email.com" já cadastrado no sistema
- **Objetivo:** Validar rejeição de email duplicado
- **Resultado esperado:** Sistema rejeita com mensagem "Email já cadastrado"
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US01-CT05 — Cadastro com email em formato inválido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar rejeição de email mal formatado
- **Resultado esperado:** Sistema rejeita com mensagem de erro de formato de email
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT06 — Cadastro sem preencher nome
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar obrigatoriedade do campo nome
- **Resultado esperado:** Sistema rejeita com mensagem indicando campo nome obrigatório
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT07 — Cadastro sem preencher email
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar obrigatoriedade do campo email
- **Resultado esperado:** Sistema rejeita com mensagem indicando campo email obrigatório
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT08 — Cadastro sem selecionar papel
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar obrigatoriedade do campo papel
- **Resultado esperado:** Sistema rejeita com mensagem indicando campo papel obrigatório
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT09 — Cadastro com papel inválido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar rejeição de valor de papel não permitido
- **Resultado esperado:** Sistema rejeita com mensagem de papel inválido
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT10 — Cadastro com nome vazio (apenas espaços)
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar tratamento de nome com apenas espaços em branco
- **Resultado esperado:** Sistema rejeita com mensagem de nome inválido ou obrigatório
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT11 — Cadastro com email diferindo apenas em maiúsculas/minúsculas
- **Pré-condição:** Admin autenticado; email "JOAO@EMAIL.COM" já cadastrado no sistema
- **Objetivo:** Validar sensibilidade a caso no email duplicado
- **Resultado esperado:** Sistema rejeita com mensagem "Email já cadastrado"
- **Tipo:** alternativo
- **Critérios cobertos:** AC2

### US01-CT12 — Cadastro com nome excedendo limite máximo
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar limite de caracteres do campo nome
- **Resultado esperado:** Sistema rejeita com mensagem de tamanho máximo excedido
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT13 — Cadastro com email excedendo limite máximo
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar limite de caracteres do campo email
- **Resultado esperado:** Sistema rejeita com mensagem de tamanho máximo excedido
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT14 — Cadastro com caracteres especiais no nome
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar aceitação de caracteres especiais válidos no nome
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida
- **Tipo:** alternativo
- **Critérios cobertos:** AC1