### US04-CT01 — Desativar usuário ativo com sucesso
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; Usuário 'monitor_ativo' está ativo no sistema e visível para desativação.
- **Objetivo:** Verificar que um admin consegue desativar com sucesso um usuário que está ativo.
- **Resultado esperado:** O acesso do usuário 'monitor_ativo' é desativado (status alterado para inativo); Sistema exibe uma mensagem de sucesso ou notificação de desativação.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US04-CT02 — Tentar desativar usuário já desativado
- **Pré-condição:** Admin autenticado na tela de gestão de usuários (ou enviando uma requisição); Usuário 'monitor_desativado' já está desativado no sistema.
- **Objetivo:** Validar que o sistema impede a desativação de um usuário que já está inativo e retorna um erro apropriado.
- **Resultado esperado:** Sistema retorna uma mensagem de erro (e.g., "Usuário já está desativado") ou um código de erro apropriado; O status do usuário 'monitor_desativado' permanece inativo.
- **Tipo:** exceção
- **Critérios cobertos:** Cenário 2