### US04-CT01 — Desativar usuário ativo com sucesso
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; usuário alvo existe e está ativo
- **Objetivo:** Validar desativação de usuário ativo pelo admin
- **Resultado esperado:** Sistema desativa o acesso do usuário e confirma a operação
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US04-CT02 — Tentar desativar usuário já desativado
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; usuário alvo existe e já está desativado
- **Objetivo:** Validar tratamento de erro ao desativar usuário inativo
- **Resultado esperado:** Sistema retorna erro informando que o usuário já está desativado
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2

### US04-CT03 — Tentar desativar usuário inexistente
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; ID de usuário inexistente informado
- **Objetivo:** Validar comportamento ao desativar usuário que não existe (partição: usuário inexistente)
- **Resultado esperado:** Sistema retorna erro de usuário não encontrado
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US04-CT04 — Admin tenta desativar a si mesmo
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; admin seleciona o próprio usuário para desativar
- **Objetivo:** Validar regra de auto-desativação (partição: usuário alvo = admin logado)
- **Resultado esperado:** Sistema impede a auto-desativação ou solicita confirmação especial
- **Tipo:** fronteira
- **Critérios cobertos:** a confirmar

### US04-CT05 — Usuário não-admin tenta acessar função de desativar
- **Pré-condição:** Usuário com perfil não-admin autenticado; tenta acessar endpoint/tela de desativação
- **Objetivo:** Validar controle de autorização (partição: perfil sem permissão de admin)
- **Resultado esperado:** Sistema nega acesso (403/redirect) e não executa desativação
- **Tipo:** segurança
- **Critérios cobertos:** a confirmar

### US04-CT06 — Desativação com sessão admin expirada
- **Pré-condição:** Admin com sessão expirada/inválida; envia requisição de desativação
- **Objetivo:** Validar proteção por autenticação (partição: admin não autenticado)
- **Resultado esperado:** Sistema rejeita a requisição (401/redirect login)
- **Tipo:** segurança
- **Critérios cobertos:** a confirmar