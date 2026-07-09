### US04-CT01 — Desativar usuário ativo com sucesso
- **Pré-condição:** Admin autenticado na tela de gestão de usuários. Usuário alvo cadastrado e ativo.
- **Objetivo:** Validar a desativação bem-sucedida de um usuário ativo por um admin.
- **Resultado esperado:** O acesso do usuário alvo é desativado e o usuário não consegue mais acessar o sistema.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US04-CT02 — Tentar desativar usuário já desativado
- **Pré-condição:** Admin autenticado na tela de gestão de usuários. Usuário alvo cadastrado e já desativado.
- **Objetivo:** Validar que o sistema impede a desativação de um usuário que já está desativado.
- **Resultado esperado:** O sistema retorna uma mensagem de erro informando que o usuário já está desativado. O estado do usuário alvo permanece desativado.
- **Tipo:** alternativo/erro
- **Critérios cobertos:** Cenário 2