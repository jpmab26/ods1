### US01-CT01 — Cadastro de usuário com perfil aluno válido
- **Pré‑condição:** Admin autenticado e na tela de gestão de usuários; email a ser cadastrado ainda não existe no sistema.
- **Objetivo:** Verificar criação de usuário com perfil **aluno**.
- **Resultado esperado:** Sistema cria o usuário com status **Pendente**, exibe senha temporária ao admin e permanece na tela de gestão.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT02 — Cadastro de usuário com perfil professor válido
- **Pré‑condição:** Admin autenticado e na tela de gestão de usuários; email não cadastrado.
- **Objetivo:** Verificar criação de usuário com perfil **professor**.
- **Resultado esperado:** Usuário criado com status **Pendente**, senha temporária exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT03 — Cadastro de usuário com perfil admin válido
- **Pré‑condição:** Admin autenticado e na tela de gestão de usuários; email ainda inexistente.
- **Objetivo:** Verificar criação de usuário com perfil **admin**.
- **Resultado esperado:** Usuário criado com status **Pendente**, senha temporária exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US01-CT04 — Rejeição de cadastro com email já existente
- **Pré‑condição:** Admin autenticado; email a ser cadastrado já pertence a outro usuário no sistema.
- **Objetivo:** Garantir que o sistema impede duplicidade de email.
- **Resultado esperado:** Cadastro é rejeitado e mensagem **‘Email já cadastrado’** é exibida ao admin.
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US01-CT05 — Campo nome vazio
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Testar validação de campo obrigatório **nome**.
- **Resultado esperado:** Sistema impede o cadastro e exibe mensagem de erro indicando que o nome é obrigatório.
- **Tipo:** robustez
- **Critérios cobertos:** a confirmar

### US01-CT06 — Campo email vazio
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários.
- **Objetivo:** Testar validação de campo obrigatório **email**.
- **Resultado esperado:** Sistema impede o cadastro e exibe mensagem de erro informando que o email é obrigatório.
- **Tipo:** robustez
- **Critérios cobertos:** a confirmar

### US01-CT07 — Formato de email inválido
- **Pré‑condição:** Admin autenticado; email digitado não segue padrão (ex.: “usuario@dominio” sem TLD).
- **Objetivo:** Verificar validação de formato de email.
- **Resultado esperado:** Sistema rejeita o cadastro e mostra mensagem de erro de email inválido.
- **Tipo:** robustez
- **Critérios cobertos:** a confirmar

### US01-CT08 — Papel não selecionado
- **Pré‑condição:** Admin autenticado; campos nome e email preenchidos, mas nenhum papel escolhido.
- **Objetivo:** Garantir que a seleção de papel é obrigatória.
- **Resultado esperado:** Sistema impede o cadastro e apresenta mensagem de erro indicando que o papel deve ser selecionado.
- **Tipo:** robustez
- **Critérios cobertos:** a confirmar

### US01-CT09 — Senha temporária gerada segue política mínima (8 caracteres)
- **Pré‑condição:** Admin autenticado; cadastro de usuário com dados válidos.
- **Objetivo:** Confirmar que a senha temporária exibida possui no mínimo 8 caracteres.
- **Resultado esperado:** Sistema exibe senha temporária com 8 ou mais caracteres.
- **Tipo:** não‑funcional
- **Critérios cobertos:** a confirmar

### US01-CT10 — Cancelamento do cadastro antes da confirmação
- **Pré‑condição:** Admin autenticado; preenchimento parcial dos campos (nome, email, papel) e aciona “Cancelar”.
- **Objetivo:** Verificar comportamento ao cancelar operação.
- **Resultado esperado:** Nenhum usuário é criado; sistema retorna à tela de gestão sem mensagens de erro.
- **Tipo:** fluxo alternativo
- **Critérios cobertos:** a confirmar