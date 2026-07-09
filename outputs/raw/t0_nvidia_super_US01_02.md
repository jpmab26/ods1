### US01-CT01 — Cadastro de usuário aluno com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar criação bem-sucedida de usuário com papel aluno
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastro de usuário professor com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar criação bem-sucedida de usuário com papel professor
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** alternativa
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastro de usuário admin com dados válidos
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar criação bem-sucedida de usuário com papel admin
- **Resultado esperado:** Usuário criado com status Pendente e senha temporária exibida ao admin
- **Tipo:** alternativa
- **Critérios cobertos:** AC1

### US01-CT04 — Tentativa de cadastro com e-mail já existente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; existe usuário com e-mail "existing@exemplo.com"
- **Objetivo:** Validar rejeição de e-mail duplicado
- **Resultado esperado:** Sistema exibe mensagem "Email já cadastrado" e não cria o usuário
- **Tipo:** negativo
- **Critérios cobertos:** AC2

### US01-CT05 — Tentativa de cadastro com e-mail em formato inválido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar comportamento ao informar e-mail fora do padrão esperado
- **Resultado esperado:** a confirmar (regras de validação de formato de e-mail não especificadas na user story)
- **Tipo:** a confirmar
- **Critérios cobertos:** a confirmar

### US01-CT06 — Tentativa de cadastro com nome vazio
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar comportamento ao deixar o nome em branco
- **Resultado esperado:** a confirmar (regras de validação de nome não especificadas na user story)
- **Tipo:** a confirmar
- **Critérios cobertos:** a confirmar

### US01-CT07 — Tentativa de cadastro com papel não previsto (ex.: coordenador)
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar comportamento ao informar papel diferente de aluno, professor ou admin
- **Resultado esperado:** a confirmar (regras de validação de papel não especificadas na user story)
- **Tipo:** a confirmar
- **Critérios cobertos:** a confirmar

### US01-CT08 — Tentativa de cadastro sem estar autenticado como admin
- **Pré-condição:** Usuário não autenticado ou autenticado com papel não-admin na tela de gestão de usuários
- **Objetivo:** Verificar se o sistema impede a operação quando o admin não está autenticado
- **Resultado esperado:** a confirmar (regras de autorização não especificadas na user story)
- **Tipo:** a confirmar
- **Critérios cobertos:** a confirmar