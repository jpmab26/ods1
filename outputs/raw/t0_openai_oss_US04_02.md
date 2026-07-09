### US04-CT01 — Desativar usuário ativo com sucesso
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários; usuário alvo está cadastrado e com status **ativo**.
- **Objetivo:** Verificar que o admin pode desativar um usuário ativo.
- **Resultado esperado:** O status do usuário passa a **desativado**; mensagem de confirmação “Usuário desativado com sucesso” é exibida; o usuário não consegue mais efetuar login.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US04-CT02 — Tentativa de desativar usuário já desativado
- **Pré‑condição:** Admin autenticado na tela de gestão de usuários; usuário alvo está cadastrado e com status **desativado**.
- **Objetivo:** Garantir que o sistema impede desativação redundante e informa o erro apropriado.
- **Resultado esperado:** Sistema retorna erro “Usuário já está desativado”; o status do usuário permanece **desativado**.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2

### US04-CT03 — Admin não autenticado tenta desativar usuário
- **Pré‑condição:** Usuário não está autenticado como admin (sessão inexistente ou token inválido).
- **Objetivo:** Verificar controle de acesso à funcionalidade de desativação.
- **Resultado esperado:** Sistema redireciona para a página de login ou retorna erro “Acesso negado – admin não autenticado”.
- **Tipo:** secundário
- **Critérios cobertos:** a confirmar (acesso à tela de gestão de usuários)

### US04-CT04 — Admin tenta desativar usuário inexistente
- **Pré‑condição:** Admin autenticado; ID do usuário informado não corresponde a nenhum registro no banco.
- **Objetivo:** Avaliar tratamento de parâmetro inválido.
- **Resultado esperado:** Sistema retorna erro “Usuário não encontrado”; nenhuma alteração de status ocorre.
- **Tipo:** secundário
- **Critérios cobertos:** a confirmar (validação de existência do usuário)

### US04-CT05 — Desativar usuário ativo com dados de sessão expirados durante a operação
- **Pré‑condção:** Admin autenticado; usuário alvo está **ativo**; durante a requisição a sessão do admin expira.
- **Objetivo:** Checar o comportamento do sistema quando a sessão expira no meio da operação.
- **Resultado esperado:** Operação é cancelada; sistema informa “Sessão expirada, faça login novamente”; o usuário permanece **ativo**.
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar (gerenciamento de timeout de sessão)

### US04-CT06 — Desativar usuário ativo com permissão insuficiente (admin de nível limitado)
- **Pré‑condição:** Usuário logado possui perfil “admin limitado” (não tem permissão para gerenciar usuários); usuário alvo está **ativo**.
- **Objetivo:** Verificar controle granular de permissões.
- **Resultado esperado:** Sistema retorna erro “Permissão negada – usuário não autorizado a desativar contas”; o status do usuário permanece **ativo**.
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar (restrição por nível de admin)

### US04-CT07 — Desativar usuário ativo via chamada API com payload correto
- **Pré‑condição:** Admin autenticado (token válido); usuário alvo está **ativo**; payload JSON contém campo `user_id` válido.
- **Objetivo:** Testar a camada de serviço (API) de desativação.
- **Resultado esperado:** Resposta HTTP 200 com corpo `{ "message": "Usuário desativado", "user_id": X }`; banco reflete status **desativado**.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US04-CT08 — Desativar usuário ativo via API com campo `user_id` ausente
- **Pré‑condição:** Admin autenticado (token válido).
- **Objetivo:** Avaliar validação de entrada da API.
- **Resultado esperado:** Resposta HTTP 400 com erro “Campo user_id obrigatório”; nenhum usuário é alterado.
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar (validação de payload)

### US04-CT09 — Desativar usuário ativo com conflito de concorrência
- **Pré‑condição:** Dois admins autenticados simultaneamente; o usuário alvo está **ativo**.
- **Objetivo:** Verificar consistência quando dois admins tentam desativar o mesmo usuário ao mesmo tempo.
- **Resultado esperado:** Primeiro request executa com sucesso (status → desativado); segundo request recebe erro “Usuário já está desativado” ou código 409 Conflict; banco mantém status **desativado**.
- **Tipo:** robustez
- **Critérios cobertos:** Cenário 2 (conflito de estado)