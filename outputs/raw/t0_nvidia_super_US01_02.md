### US01-CT01 — Cadastro bem-sucedido de usuário aluno
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; nenhum usuário com o mesmo email existe no sistema.
- **Objetivo:** Validar que o sistema cria usuário com status Pendente e exibe senha temporária ao admin ao preencher nome, email e papel válidos (aluno).
- **Resultado esperado:** Usuário é criado, aparece na lista com status Pendente, e uma senha temporária é exibida ao admin (ex.: em modal ou toast).
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastro bem-sucedido de usuário professor
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; nenhum usuário com o mesmo email existe no sistema.
- **Objetivo:** Validar que o sistema cria usuário com status Pendente e exibe senha temporária ao admin ao preencher nome, email e papel válidos (professor).
- **Resultado esperado:** Usuário é criado, aparece na lista com status Pendente, e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastro bem-sucedido de usuário admin
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; nenhum usuário com o mesmo email existe no sistema.
- **Objetivo:** Validar que o sistema cria usuário com status Pendente e exibe senha temporária ao admin ao preencher nome, email e papel válidos (admin).
- **Resultado esperado:** Usuário é criado, aparece na lista com status Pendente, e uma senha temporária é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT04 — Rejeição de cadastro com email já existente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; já existe um usuário com o email informado no sistema.
- **Objetivo:** Verificar que o sistema impede o cadastro de usuário com email duplicado e exibe mensagem adequada.
- **Resultado esperado:** Sistema rejeita o cadastro, não cria o usuário e exibe a mensagem "Email já cadastrado".
- **Tipo:** alternativo
- **Critérios cobertos:** AC2 (Given-When-Then segundo cenário)

### US01-CT05 — Tentativa de cadastro com nome vazio (ambiguidade)
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; email informado não existe no sistema.
- **Objetivo:** Verificar comportamento do sistema quando o campo nome está vazio (não especificado na user story).
- **Resultado esperado:** a confirmar
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT06 — Tentativa de cadastro com email em formato inválido (ambiguidade)
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; nome e papel válidos informados.
- **Objetivo:** Verificar comportamento do sistema quando o email está em formato inválido (não especificado na user story).
- **Resultado esperado:** a confirmar
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US01-CT07 — Tentativa de cadastro com papel inválido (ambiguidade)
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; nome e email válidos e não duplicados informados.
- **Objetivo:** Verificar comportamento do sistema quando o papel informado não é um dos esperados (aluno, professor, admin) (não especificado na user story).
- **Resultado esperado:** a confirmar
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar