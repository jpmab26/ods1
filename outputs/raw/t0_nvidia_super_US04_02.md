### US04-CT01 — Desativa usuário ativo
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; existe pelo menos um usuário com status ativo.
- **Objetivo:** Validar que o admin consegue desativar um usuário ativo.
- **Resultado esperado:** O acesso do usuário selecionado é alterado para inativo; sistema exibe mensagem de sucesso.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US04-CT02 — Tenta desativar usuário já desativado
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; existe um usuário com status já inativo.
- **Objetivo:** Verificar que o sistema impede a desativação de um usuário já inativo.
- **Resultado esperado:** Sistema retorna erro indicando que o usuário já está desativado; nenhum cambio de estado ocorre.
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US04-CT03 — Admin não autenticado tenta desativar usuário
- **Pré-condição:** Não há sessão de admin autenticado; tenta acessar a funcionalidade de desativação via requisição direta.
- **Objetivo:** Verificar comportamento quando admin não autenticado tenta executar a ação.
- **Resultado esperado:** Sistema nega o acesso (redireciona para login ou retorna erro de autorização). Como a história não especifica explicitamente o requisito de autenticação para este caso, marcamos a confirmação necessária.
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US04-CT04 — Tentativa de desativar usuário inexistente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; tenta desativar um ID de usuário que não está cadastrado.
- **Objetivo:** Verificar tratamento de tentativa de desativar usuário inexistente.
- **Resultado esperado:** Sistema retorna erro indicando que o usuário não foi encontrado. Como a história não trata desse caso, marcamos a confirmação necessária.
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar