### US04-CT01 — Desativar usuário ativo
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; existe pelo menos um usuário ativo no sistema.
- **Objetivo:** Verificar que o sistema desativa o acesso do usuário selecionado.
- **Resultado esperado:** O status do usuário muda para "desativado" e o sistema exibe confirmação de desativação.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US04-CT02 — Tentativa de desativar usuário já desativado
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; existe um usuário com status já desativado.
- **Objetivo:** Verificar que o sistema impede a desativação e retorna erro apropriado.
- **Resultado esperado:** Sistema exibe mensagem de erro indicando que o usuário já está desativado e não altera o status.
- **Tipo:** alternativo
- **Critérios cobertos:** AC2

### US04-CT03 — Tentativa de desativar usuário sem autenticação de admin
- **Pré-condição:** Não há admin autenticado; usuário tenta acessar endpoint de desativação diretamente.
- **Objetivo:** Verificar comportamento quando admin não está autenticado (regras não especificadas na US).
- **Resultado esperado:** a confirmar
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar

### US04-CT04 — Tentativa de desativar usuário inexistente
- **Pré-condição:** Admin autenticado; tenta desativar usuário com ID não cadastrado.
- **Objetivo:** Verificar tratamento de usuário inexistente (não especificado na US).
- **Resultado esperado:** a confirmar
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar