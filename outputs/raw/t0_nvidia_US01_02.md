### US01-CT01 — Cadastro de aluno com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel aluno
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** Critério 1

### US01-CT02 — Cadastro de professor com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel professor
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** Critério 1

### US01-CT03 — Cadastro de admin com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel admin
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** Critério 1

### US01-CT04 — Tentativa de cadastro com email já existente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; email já cadastrado na base
- **Objetivo:** Validar rejeição de email duplicado
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem 'Email já cadastrado'
- **Tipo:** erro
- **Critérios cobertos:** Critério 2

### US01-CT05 — Cadastro com email em formato inválido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar tratamento de email com formato inválido (ex.: 'usuario@', 'usuario.com')
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de erro de validação de email
- **Tipo:** erro
- **Critérios cobertos:** a confirmar

### US01-CT06 — Cadastro com nome vazio
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar obrigatoriedade do campo nome
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de erro indicando nome obrigatório
- **Tipo:** erro
- **Critérios cobertos:** a confirmar

### US01-CT07 — Cadastro com papel inválido ou não selecionado
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar obrigatoriedade e validação do campo papel
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de erro indicando papel inválido ou obrigatório
- **Tipo:** erro
- **Critérios cobertos:** a confirmar

### US01-CT08 — Cadastro sem preencher email
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar obrigatoriedade do campo email
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de erro indicando email obrigatório
- **Tipo:** erro
- **Critérios cobertos:** a confirmar

### US01-CT09 — Verificação de status Pendente e senha temporária exibida
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; cadastro realizado com sucesso (dados válidos)
- **Objetivo:** Confirmar que o usuário é criado com status Pendente e que a senha temporária é exibida ao admin
- **Resultado esperado:** Usuário aparece na lista com status Pendente; senha temporária visível na tela de confirmação
- **Tipo:** principal
- **Critérios cobertos:** Critério 1

### US01-CT10 — Cadastro com nome com comprimento máximo permitido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar aceitação de nome no limite superior de caracteres (se houver regra de tamanho)
- **Resultado esperado:** Sistema aceita o cadastro e cria usuário com status Pendente
- **Tipo:** borda
- **Critérios cobertos:** a confirmar

### US01-CT11 — Cadastro com nome excedendo comprimento máximo permitido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar rejeição de nome que excede o limite superior de caracteres (se houver regra de tamanho)
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de erro de validação de tamanho do nome
- **Tipo:** borda
- **Critérios cobertos:** a confirmar