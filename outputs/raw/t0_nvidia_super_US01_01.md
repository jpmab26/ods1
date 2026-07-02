### US01-CT01 — Cadastro bem-sucedido de usuário aluno
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel aluno, status Pendente e exibição de senha temporária
- **Resultado esperado:** Sistema cria o usuário, define status como Pendente e exibe a senha temporária ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastro bem-sucedido de usuário professor
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel professor, status Pendente e exibição de senha temporária
- **Resultado esperado:** Sistema cria o usuário, define status como Pendente e exibe a senha temporária ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastro bem-sucedido de usuário admin
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Validar criação de usuário com papel admin, status Pendente e exibição de senha temporária
- **Resultado esperado:** Sistema cria o usuário, define status como Pendente e exibe a senha temporária ao admin
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT04 — Tentativa de cadastro com nome vazio
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar comportamento do sistema quando o campo nome está vazio
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de erro indicando que o nome é obrigatório
- **Tipo:** alternativa
- **Critérios cobertos:** a confirmar

### US01-CT05 — Tentativa de cadastro com e-mail inválido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar comportamento do sistema quando o e-mail tem formato inválido
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de erro indicando formato de e-mail inválido
- **Tipo:** alternativa
- **Critérios cobertos:** a confirmar

### US01-CT06 — Tentativa de cadastro com papel não permitido
- **Pré-condição:** Admin autenticado na tela de gestão de usuários
- **Objetivo:** Verificar comportamento do sistema quando o papel informado não está entre os valores permitidos (aluno, professor, admin)
- **Resultado esperado:** Sistema rejeita o cadastro e exibe mensagem de erro indicando papel inválido
- **Tipo:** alternativa
- **Critérios cobertos:** a confirmar

### US01-CT07 — Tentativa de cadastro com e-mail já existente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; já existe um usuário cadastrado com o e-mail a ser utilizado
- **Objetivo:** Validar rejeição de cadastro de e-mail duplicado
- **Resultado esperado:** Sistema impede a criação e exibe a mensagem 'Email já cadastrado'
- **Tipo:** alternativa
- **Critérios cobertos:** AC2

### US01-CT08 — Verificação de status e senha temporária após criação
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; cadastro realizado com dados válidos
- **Objetivo:** Confirmar que o usuário criado possui status Pendente e que a senha temporária é exibida apenas uma vez
- **Resultado esperado:** Na lista de usuários, o novo registro aparece com status Pendente; a senha temporária é mostrada na tela de confirmação e não está disponível em demais telas
- **Tipo:** principal
- **Critérios cobertos:** AC1