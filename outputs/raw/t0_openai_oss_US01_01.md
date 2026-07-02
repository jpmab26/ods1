### US01-CT01 — Cadastro de usuário com dados válidos (perfil Aluno)  
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários  
- **Objetivo:** Verificar criação de usuário com perfil “aluno” utilizando informações corretas  
- **Resultado esperado:** Usuário é criado com status **Pendente** e senha temporária exibida ao admin  
- **Tipo:** principal  
- **Critérios cobertos:** AC1  

### US01-CT02 — Cadastro de usuário com dados válidos (perfil Professor)  
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários  
- **Objetivo:** Verificar criação de usuário com perfil “professor” utilizando informações corretas  
- **Resultado esperado:** Usuário é criado com status **Pendente** e senha temporária exibida ao admin  
- **Tipo:** principal  
- **Critérios cobertos:** AC1  

### US01-CT03 — Cadastro de usuário com dados válidos (perfil Admin)  
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários  
- **Objetivo:** Verificar criação de usuário com perfil “admin” utilizando informações corretas  
- **Resultado esperado:** Usuário é criado com status **Pendente** e senha temporária exibida ao admin  
- **Tipo:** principal  
- **Critérios cobertos:** AC1  

### US01-CT04 — Tentativa de cadastro com e‑mail já existente  
- **Pré‑condição:** Admin autenticado; e‑mail “existente@uni.edu” já cadastrado no sistema  
- **Objetivo:** Garantir que o sistema rejeite o cadastro de e‑mail duplicado  
- **Resultado esperado:** Mensagem de erro **“Email já cadastrado”** exibida; nenhum usuário novo é criado  
- **Tipo:** principal  
- **Critérios cobertos:** AC2  

### US01-CT05 — Campo Nome vazio  
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários  
- **Objetivo:** Validar comportamento ao enviar cadastro sem preencher o campo Nome  
- **Resultado esperado:** Mensagem de validação indicando campo Obrigatório; cadastro não é concluído  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT06 — Campo E‑mail vazio  
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários  
- **Objetivo:** Validar comportamento ao enviar cadastro sem preencher o campo E‑mail  
- **Resultado esperado:** Mensagem de validação indicando campo Obrigatório; cadastro não é concluído  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT07 — Formato de e‑mail inválido  
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários  
- **Objetivo:** Verificar rejeição de e‑mail fora do padrão RFC 5322 (ex.: “usuario@@dominio.com”)  
- **Resultado esperado:** Mensagem de erro “E‑mail inválido”; cadastro não é concluído  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT08 — Nome com tamanho máximo excedido (256 caracteres)  
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários  
- **Objetivo:** Avaliar limite de tamanho do campo Nome  
- **Resultado esperado:** Mensagem de erro indicando que o nome ultrapassa o limite permitido; cadastro não é concluído  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT09 — Seleção de papel fora das opções permitidas  
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários  
- **Objetivo:** Testar comportamento ao tentar cadastrar com papel não reconhecido (ex.: “coordenador”)  
- **Resultado esperado:** Sistema recusa entrada com mensagem “Papel inválido”; nenhum usuário é criado  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT10 — Cancelamento do cadastro antes da confirmação  
- **Pré‑condição:** Admin autenticado; campos preenchidos parcialmente  
- **Objetivo:** Garantir que ao cancelar a operação o registro não seja salvo  
- **Resultado esperado:** Tela retorna à lista de usuários; nenhum novo usuário é criado; nenhuma senha temporária é exibida  
- **Tipo:** secundário  
- **Critérios cobertos:** a confirmar  

### US01-CT11 — Conexão com banco de dados indisponível no momento do cadastro  
- **Pré‑condição:** Admin autenticado; banco MySQL offline  
- **Objetivo:** Verificar tratamento de falha de persistência de dados  
- **Resultado esperado:** Mensagem de erro genérica “Não foi possível cadastrar o usuário no momento”; operação não confirma a criação nem gera senha temporária  
- **Tipo:** negativo  
- **Critérios cobertos:** a confirmar  

### US01-CT12 — Cadastro simultâneo de dois usuários com o mesmo e‑mail (condição de corrida)  
- **Pré‑condição:** Dois admins diferentes autenticados em sessões paralelas; e‑mail ainda não existente  
- **Objetivo:** Garantir que o mecanismo de unicidade no banco impeça duplicação mesmo em concorrência  
- **Resultado esperado:** Um dos cadastros é concluído com sucesso; o outro recebe mensagem “Email já cadastrado” e não cria usuário  
- **Tipo:** desempenho / concorrência  
- **Critérios cobertos:** AC2  

---  

*Obs.: Casos marcados como “a confirmar” tratam de regras que não constam explicitamente na user story e deverão ser validadas com o Product Owner.*