### US04-CT01 — Desativar usuário com status ativo
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; usuário alvo cadastrado e com status **ativo**
- **Objetivo:** Validar desativação bem-sucedida de usuário ativo
- **Resultado esperado:** Sistema altera status do usuário para inativo, remove acesso e exibe confirmação
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US04-CT02 — Tentar desativar usuário já desativado
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; usuário alvo cadastrado e com status **inativo**
- **Objetivo:** Validar tratamento de erro ao desativar usuário já inativo
- **Resultado esperado:** Sistema não altera estado, retorna mensagem de erro informando que usuário já está desativado
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2

### US04-CT03 — Tentar desativar usuário inexistente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; ID de usuário que não existe na base
- **Objetivo:** Validar comportamento ao solicitar desativação de ID inexistente (partição de equivalência: usuário inexistente)
- **Resultado esperado:** Sistema retorna erro de recurso não encontrado
- **Tipo:** exceção
- **Critérios cobertos:** a confirmar

### US04-CT04 — Usuário não-admin tenta desativar outro usuário
- **Pré-condição:** Usuário com perfil **monitor/coordenador** (não admin) autenticado; usuário alvo ativo
- **Objetivo:** Validar restrição de permissão para ação administrativa (partição de equivalência: ator sem permissão)
- **Resultado esperado:** Sistema nega acesso (403/redirecionamento) e não altera status do alvo
- **Tipo:** exceção
- **Critérios cobertos:** a confirmar

### US04-CT05 — Admin tenta desativar a si mesmo
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; admin seleciona o próprio usuário (ativo)
- **Objetivo:** Validar regra de auto-desativação (partição de equivalência: alvo = ator)
- **Resultado esperado:** Sistema impede a ação e exibe aviso, ou permite e encerra sessão (conforme regra não documentada)
- **Tipo:** borda
- **Critérios cobertos:** a confirmar