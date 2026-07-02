### US01-CT01 — Cadastro de aluno com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel 'aluno' e exibição de senha temporária
- **Resultado esperado:** Usuário criado com status 'Pendente'; senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastro de professor com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel 'professor'
- **Resultado esperado:** Usuário criado com status 'Pendente'; senha temporária exibida ao admin
- **Tipo:** alternativo
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastro de admin com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel 'admin'
- **Resultado esperado:** Usuário criado com status 'Pendente'; senha temporária exibida ao admin
- **Tipo:** alternativo
- **Critérios cobertos:** AC1

### US01-CT04 — Cadastro com email já existente
- **Pré-condição:** Admin autenticado; email 'existente@teste.com' já cadastrado na base
- **Objetivo:** Validar rejeição de email duplicado
- **Resultado esperado:** Sistema rejeita cadastro e exibe mensagem 'Email já cadastrado'
- **Tipo:** erro
- **Critérios cobertos:** AC2

### US01-CT05 — Cadastro com formato de email inválido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar rejeição de email com sintaxe incorreta (ex: 'usuario@', '@dominio.com')
- **Resultado esperado:** Sistema rejeita cadastro com mensagem de validação de formato de email
- **Tipo:** erro
- **Critérios cobertos:** a confirmar

### US01-CT06 — Cadastro com nome em branco
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar campo nome obrigatório
- **Resultado esperado:** Sistema rejeita cadastro e indica erro no campo nome
- **Tipo:** erro
- **Critérios cobertos:** a confirmar

### US01-CT07 — Cadastro com email em branco
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar campo email obrigatório
- **Resultado esperado:** Sistema rejeita cadastro e indica erro no campo email
- **Tipo:** erro
- **Critérios cobertos:** a confirmar

### US01-CT08 — Cadastro com papel não selecionado
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar campo papel obrigatório
- **Resultado esperado:** Sistema rejeita cadastro e indica erro no campo papel
- **Tipo:** erro
- **Critérios cobertos:** a confirmar

### US01-CT09 — Cadastro com papel inválido (valor fora da lista)
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; requisição interceptada com papel 'coordenador'
- **Objetivo:** Validar restrição de valores permitidos para papel
- **Resultado esperado:** Sistema rejeita cadastro com erro de valor inválido para papel
- **Tipo:** erro
- **Critérios cobertos:** a confirmar

### US01-CT10 — Cadastro com nome excedendo limite de caracteres
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; nome com 256 caracteres (limite hipotético 255)
- **Objetivo:** Validar tamanho máximo do campo nome
- **Resultado esperado:** Sistema rejeita cadastro com mensagem de tamanho excedido
- **Tipo:** borda
- **Critérios cobertos:** a confirmar

### US01-CT11 — Tentativa de acesso à tela de cadastro sem autenticação
- **Pré-condição:** Usuário não autenticado acessa URL direta de cadastro de usuários
- **Objetivo:** Validar controle de acesso à funcionalidade restrita a admins
- **Resultado esperado:** Sistema redireciona para login ou exibe erro 403/401
- **Tipo:** segurança
- **Critérios cobertos:** a confirmar

### US01-CT12 — Verificação de status inicial 'Pendente' no banco de dados
- **Pré-condição:** Admin autenticado; cadastro de aluno realizado com sucesso (CT01)
- **Objetivo:** Confirmar persistência do status inicial
- **Resultado esperado:** Registro na tabela de usuários apresenta status 'Pendente'
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT13 — Verificação de exibição de senha temporária única
- **Pré-condição:** Admin autenticado; cadastro realizado com sucesso
- **Objetivo:** Confirmar que senha temporária é exibida apenas no momento da criação
- **Resultado esperado:** Senha temporária visível na tela de sucesso; ao recarregar ou sair, não mais exibida
- **Tipo:** alternativo
- **Critérios cobertos:** AC1