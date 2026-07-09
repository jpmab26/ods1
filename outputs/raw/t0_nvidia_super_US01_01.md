### US01-CT01 — Cadastro de usuário aluno com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar criação de usuário com papel aluno
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastro de usuário professor com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar criação de usuário com papel professor
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastro de usuário admin com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar criação de usuário com papel admin
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT04 — Cadastro com nome vazio
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar comportamento ao deixar o nome em branco
- **Resultado esperado:** Sistema rejeita o cadastro (mensagem de erro a confirmar)
- **Tipo:** exceção
- **Critérios cobertos:** a confirmar

### US01-CT05 — Cadastro com email vazio
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar comportamento ao deixar o email em branco
- **Resultado esperado:** Sistema rejeita o cadastro (mensagem de erro a confirmar)
- **Tipo:** exceção
- **Critérios cobertos:** a confirmar

### US01-CT06 — Cadastro com papel inválido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar comportamento ao informar papel diferente de aluno, professor ou admin
- **Resultado esperado:** Sistema rejeita o cadastro (mensagem de erro a confirmar)
- **Tipo:** exceção
- **Critérios cobertos:** a confirmar

### US01-CT07 — Cadastro com email já existente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; existir usuário com o mesmo email cadastrado
- **Objetivo:** Verificar tratamento de email duplicado
- **Resultado esperado:** Sistema rejeita o cadastro com mensagem 'Email já cadastrado'
- **Tipo:** alternativa
- **Critérios cobertos:** AC2

### US01-CT08 — Cadastro com email em formato inválido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar comportamento ao inserir email com formato inválido (ex: sem @)
- **Resultado esperado:** Sistema rejeita o cadastro (mensagem de erro a confirmar)
- **Tipo:** exceção
- **Critérios cobertos:** a confirmar