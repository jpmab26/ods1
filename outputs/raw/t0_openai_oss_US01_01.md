### US01-CT01 — Cadastro de usuário com dados válidos (perfil aluno)  
- **Pré-condição:** Admin autenticado e na tela de gestão de usuários; email a ser cadastrado ainda não existe no sistema.  
- **Objetivo:** Verificar a criação de um usuário com perfil “aluno” usando dados corretos.  
- **Resultado esperado:** Sistema cria o usuário com status **Pendente** e exibe ao admin uma senha temporária.  
- **Tipo:** principal  
- **Critérios cobertos:** AC1  

### US01-CT02 — Cadastro de usuário com dados válidos (perfil professor)  
- **Pré-condição:** Admin autenticado e na tela de gestão de usuários; email ainda não cadastrado.  
- **Objetivo:** Verificar a criação de um usuário com perfil “professor”.  
- **Resultado esperado:** Usuário criado com status **Pendente** e senha temporária mostrada ao admin.  
- **Tipo:** principal  
- **Critérios cobertos:** AC1  

### US01-CT03 — Cadastro de usuário com dados válidos (perfil admin)  
- **Pré‑condição:** Admin autenticado; email inexistente no banco.  
- **Objetivo:** Garantir que o admin pode cadastrar outro usuário com perfil “admin”.  
- **Resultado esperado:** Usuário criado com status **Pendente** e senha temporária exibida.  
- **Tipo:** principal  
- **Critérios cobertos:** AC1  

### US01-CT04 — Tentativa de cadastro com email já existente  
- **Pré‑condição:** Admin autenticado; email já cadastrado no sistema (qualquer perfil).  
- **Objetivo:** Verificar a rejeição do cadastro quando o email já está em uso.  
- **Resultado esperado:** Sistema impede o cadastro e exibe a mensagem **“Email já cadastrado”**.  
- **Tipo:** negativo  
- **Critérios cobertos:** AC2  

### US01-CT05 — Campos obrigatórios ausentes (nome em branco)  
- **Pré‑condição:** Admin autenticado; email novo e válido.  
- **Objetivo:** Avaliar o comportamento quando o campo **nome** é deixado vazio.  
- **Resultado esperado:** Sistema impede o cadastro e apresenta mensagem de erro indicando campo obrigatório (ex.: “Nome é obrigatório”).  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar (validação de campos obrigatórios)  

### US01-CT06 — Formato de email inválido  
- **Pré‑condição:** Admin autenticado; nome preenchido e perfil válido.  
- **Objetivo:** Testar a validação de formato de email.  
- **Resultado esperado:** Sistema rejeita o cadastro e mostra mensagem de erro (ex.: “Formato de email inválido”).  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar (validação de formato de email)  

### US01-CT07 — Papel fora do conjunto permitido (ex.: “assistente”)  
- **Pré‑condição:** Admin autenticado; nome e email válidos.  
- **Objetivo:** Verificar a proteção contra papéis não permitidos.  
- **Resultado esperado:** Sistema impede o cadastro e exibe mensagem de erro (ex.: “Papel inválido”).  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar (restrição de valores de papel)  

### US01-CT08 — Dados com tamanho máximo excedido (nome > 255 caracteres)  
- **Pré‑condição:** Admin autenticado; email novo e válido.  
- **Objetivo:** Avaliar o tratamento de campos que excedem o limite de tamanho.  
- **Resultado esperado:** Sistema rejeita o cadastro e apresenta mensagem de erro (ex.: “Nome ultrapassa o tamanho permitido”).  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar (limite de tamanho de campos)