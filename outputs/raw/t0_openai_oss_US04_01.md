### US04-CT01 — Desativar usuário ativo com sucesso
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; usuário alvo está com status **ativo**.
- **Objetivo:** Verificar que o admin consegue desativar um usuário que está ativo.
- **Resultado esperado:** Sistema altera o status do usuário para **desativado**, exibe mensagem de sucesso e impede novo login desse usuário.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US04-CT02 — Tentativa de desativar usuário já desativado
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; usuário alvo já está com status **desativado**.
- **Objetivo:** Garantir que o sistema impede a desativação de um usuário já desativado.
- **Resultado esperado:** Sistema retorna erro indicando que o usuário já está desativado; status permanece **desativado**.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 2

### US04-CT03 — Desativar usuário ativo sem permissão de admin
- **Pré-condição:** Usuário autenticado que **não** possui perfil admin; tela de gestão de usuários acessada (por tentativa ou erro).
- **Objetivo:** Confirmar que apenas admins podem desativar usuários.
- **Resultado esperado:** Sistema impede a ação, exibindo mensagem de autorização negada; status do usuário alvo permanece **ativo**.
- **Tipo:** segurança
- **Critérios cobertos:** a confirmar (regra de permissão não explicitada na US)

### US04-CT04 — Desativar usuário com ID inexistente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; ID informado não corresponde a nenhum usuário cadastrado.
- **Objetivo:** Verificar o tratamento de tentativa de desativação de usuário inexistente.
- **Resultado esperado:** Sistema retorna erro “Usuário não encontrado” e não altera nenhum registro.
- **Tipo:** robustez
- **Critérios cobertos:** a confirmar (validação de existência de usuário)

### US04-CT05 — Desativar usuário ativo após sessão expirada do admin
- **Pré-condição:** Admin autenticado, mas a sessão expira antes de confirmar a desativação.
- **Objetivo:** Garantir que a ação não seja concluída se a sessão do admin não for válida.
- **Resultado esperado:** Sistema redireciona para tela de login ou exibe mensagem de sessão expirada; usuário alvo mantém status **ativo**.
- **Tipo:** fluxo
- **Critérios cobertos:** a confirmar (gerenciamento de sessão)

### US04-CT06 — Verificar registro de auditoria para desativação
- **Pré-condição:** Admin autenticado; usuário alvo está **ativo**.
- **Objetivo:** Assegurar que a operação de desativação seja registrada no log de auditoria.
- **Resultado esperado:** Após a desativação, log contém: ID do admin, ID do usuário desativado, timestamp, ação “desativar”.
- **Tipo:** não funcional
- **Critérios cobertos:** a confirmar (requisito de auditoria não explicitado)