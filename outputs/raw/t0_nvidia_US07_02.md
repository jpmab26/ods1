### US07-CT01 — Indicação bem-sucedida de aluno válido
- **Pré-condição:** Professor autenticado na tela de uma disciplina de sua responsabilidade; existe aluno com papel "aluno" cadastrado no sistema.
- **Objetivo:** Validar criação de vínculo de monitoria com status "Pendente de aprovação" ao indicar aluno elegível.
- **Resultado esperado:** Vínculo criado e exibido com status "Pendente de aprovação"; mensagem de sucesso apresentada.
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US07-CT02 — Indicação de usuário sem papel aluno
- **Pré-condição:** Professor autenticado na tela de uma disciplina de sua responsabilidade; existe usuário cadastrado sem papel "aluno" (ex.: professor, administrador, usuário externo).
- **Objetivo:** Validar rejeição da indicação quando o usuário selecionado não possui papel "aluno".
- **Resultado esperado:** Sistema impede a indicação e exibe mensagem de erro "Papel inválido" (ou similar); nenhum vínculo é criado.
- **Tipo:** principal
- **Critérios cobertos:** AC2

### US07-CT03 — Disciplina de outro professor não aparece nas opções
- **Pré-condição:** Professor autenticado; existem disciplinas de sua responsabilidade e disciplinas de outros professores cadastradas.
- **Objetivo:** Validar que apenas disciplinas do professor logado são listadas para indicação de monitor.
- **Resultado esperado:** Na tela de indicação, somente disciplinas sob responsabilidade do professor são exibidas; disciplinas de outros professores não aparecem na lista.
- **Tipo:** principal
- **Critérios cobertos:** AC3

### US07-CT04 — Indicação de aluno já vinculado como monitor na mesma disciplina
- **Pré-condição:** Professor autenticado na tela de uma disciplina de sua responsabilidade; aluno já possui vínculo de monitoria ativo ou pendente nessa disciplina.
- **Objetivo:** Verificar comportamento ao tentar indicar aluno já monitor da disciplina (regra não especificada nos critérios).
- **Resultado esperado:** Sistema impede nova indicação e exibe mensagem informativa (ex.: "Aluno já é monitor desta disciplina"); nenhum vínculo duplicado é criado.
- **Tipo:** alternativa
- **Critérios cobertos:** a confirmar

### US07-CT05 — Indicação cancelada pelo professor antes da confirmação
- **Pré-condição:** Professor autenticado na tela de indicação de monitor, com aluno válido selecionado.
- **Objetivo:** Validar que cancelamento da operação não cria vínculo.
- **Resultado esperado:** Ao clicar em "Cancelar", o professor retorna à tela da disciplina sem criar vínculo; nenhum registro é persistido.
- **Tipo:** alternativa
- **Critérios cobertos:** a confirmar

### US07-CT06 — Tentativa de indicação via manipulação de ID de disciplina de outro professor
- **Pré-condição:** Professor autenticado; conhece ID de disciplina de outro professor (ex.: via URL direta /indicar-monitor?disciplina_id=999).
- **Objetivo:** Validar controle de autorização no backend ao tentar indicar monitor para disciplina não autorizada.
- **Resultado esperado:** Sistema retorna erro 403/404 ou redireciona com mensagem de acesso negado; nenhum vínculo é criado.
- **Tipo:** segurança
- **Critérios cobertos:** a confirmar