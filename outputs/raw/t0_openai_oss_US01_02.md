### US01-CT01 — Cadastro com dados válidos (perfil aluno)  
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários; email a ser cadastrado ainda não existe no banco.  
- **Objetivo:** Verificar criação de usuário com perfil *aluno* usando informações corretas.  
- **Resultado esperado:** Sistema cria o usuário com status **Pendente** e exibe senha temporária ao admin.  
- **Tipo:** principal  
- **Critérios cobertos:** AC1  

### US01-CT02 — Cadastro com dados válidos (perfil professor)  
- **Pré‑condição:** Admin autenticado; email inexistente.  
- **Objetivo:** Verificar criação de usuário com perfil *professor*.  
- **Resultado esperado:** Usuário criado com status **Pendente** e senha temporária mostrada ao admin.  
- **Tipo:** principal  
- **Critérios cobertos:** AC1  

### US01-CT03 — Cadastro com dados válidos (perfil admin)  
- **Pré‑condição:** Admin autenticado; email inexistente.  
- **Objetivo:** Verificar criação de usuário com perfil *admin*.  
- **Resultado esperado:** Usuário criado com status **Pendente** e senha temporária exibida.  
- **Tipo:** principal  
- **Critérios cobertos:** AC1  

### US01-CT04 — Tentativa de cadastro com email já existente  
- **Pré‑condição:** Admin autenticado; email já cadastrado no sistema (qualquer perfil).  
- **Objetivo:** Garantir que o sistema impede duplicação de email.  
- **Resultado esperado:** Cadastro rejeitado com mensagem **'Email já cadastrado'**.  
- **Tipo:** negativo  
- **Critérios cobertos:** AC2  

### US01-CT05 — Campo nome vazio  
- **Pré‑condição:** Admin autenticado; email inexistente.  
- **Objetivo:** Verificar validação de campo obrigatório *nome*.  
- **Resultado esperado:** Sistema impede o cadastro e exibe mensagem de erro indicando que o nome é obrigatório.  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT06 — Campo email vazio  
- **Pré‑condição:** Admin autenticado; nome preenchido, perfil selecionado.  
- **Objetivo:** Verificar validação de campo obrigatório *email*.  
- **Resultado esperado:** Sistema impede o cadastro e mostra mensagem de erro informando que o email é obrigatório.  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT07 — Formato de email inválido  
- **Pré‑condição:** Admin autenticado; nome preenchido, perfil selecionado; email em formato inválido (ex.: `usuario@@dominio`).  
- **Objetivo:** Garantir que o sistema valida o formato do email.  
- **Resultado esperado:** Cadastro bloqueado com mensagem de erro de **email inválido**.  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT08 — Perfil não selecionado  
- **Pré‑condição:** Admin autenticado; nome e email válidos preenchidos; campo de perfil deixado em estado “seleção vazia”.  
- **Objetivo:** Validar obrigatoriedade da escolha do perfil.  
- **Resultado esperado:** Sistema impede o cadastro e apresenta mensagem indicando que o perfil deve ser escolhido.  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT09 — Nome com caracteres especiais/extremamente longo  
- **Pré‑condição:** Admin autenticado; email inexistente; perfil escolhido.  
- **Objetivo:** Avaliar limite de tamanho e aceitação de caracteres no campo nome.  
- **Resultado esperado:** Se o nome ultrapassa o limite definido (ex.: > 100 caracteres) ou contém caracteres proibidos, o sistema rejeita o cadastro com mensagem de erro apropriada; caso o limite permita, o cadastro ocorre normalmente.  
- **Tipo:** limite / negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT10 — Email com domínio não permitido (ex.: domínio institucional obrigatório)  
- **Pré‑condição:** Admin autenticado; nome preenchido; perfil escolhido; email com domínio diferente do esperado (ex.: `usuario@gmail.com`).  
- **Objetivo:** Verificar se há restrição de domínio de email (não especificado na US).  
- **Resultado esperado:** Se houver restrição, cadastro rejeitado com mensagem de domínio inválido; se não houver, usuário criado normalmente.  
- **Tipo:** negativo / a confirmar  
- **Critérios cobertos:** a confirmar  

### US01-CT11 — Cancelamento da ação de cadastro  
- **Pré‑condição:** Admin autenticado; formulário parcialmente preenchido.  
- **Objetivo:** Garantir que ao cancelar o cadastro o sistema não persiste nenhum registro.  
- **Resultado esperado:** Nenhum usuário é criado; o admin retorna à tela de gestão sem alterações.  
- **Tipo:** fluxo alternativo  
- **Critérios cobertos:** a confirmar  

### US01-CT12 — Conexão com banco de dados indisponível no momento do cadastro  
- **Pré‑condição:** Admin autenticado; dados válidos; banco de dados offline.  
- **Objetivo:** Verificar comportamento do sistema frente a falha de persistência.  
- **Resultado esperado:** Sistema exibe mensagem de erro genérica de falha ao salvar e não cria usuário.  
- **Tipo:** erro de infraestrutura  
- **Critérios cobertos:** a confirmar