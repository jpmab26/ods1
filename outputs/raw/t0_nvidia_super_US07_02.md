###US07-CT01 — Indicação bem-sucedida de aluno como monitor
- **Pré-condição:** Professor autenticado na tela de uma disciplina que lhe é responsável; disciplina possui pelo menos um aluno cadastrado com papel "aluno"
- **Objetivo:** Verificar que a indicação de um aluno como monitor cria vínculo com status "Pendente de aprovação"
- **Resultado esperado:** Sistema confirma a indicação e exibe o vínculo criado com status "Pendente de aprovação"
- **Tipo:** principal
- **Critérios cobertos:** AC1

### US07-CT02 — Indicação de usuário com papel professor (não aluno)
- **Pré-condição:** Professor autenticado na tela de uma disciplina que lhe é responsável; lista de usuários disponíveis inclui pelo menos um usuário com papel "professor"
- **Objetivo:** Validar que o sistema rejeita a indicação quando o usuário selecionado não possui papel "aluno"
- **Resultado esperado:** Sistema impede a confirmação e exibe mensagem informando que o papel do usuário é inválido para monitoria
- **Tipo:** negativo
- **Critérios cobertos:** AC2

### US07-CT03 — Indicação de usuário com papel administrativo (não aluno)
- **Pré-condição:** Professor autenticado na tela de uma disciplina que lhe é responsável; lista de usuários disponíveis inclui pelo menos um usuário com papel "administrador"
- **Objetivo:** Validar que o sistema rejeita a indicação quando o usuário selecionado não possui papel "aluno"
- **Resultado esperado:** Sistema impede a confirmação e exibe mensagem informando que o papel do usuário é inválido para monitoria
- **Tipo:** negativo
- **Critérios cobertos:** AC2

### US07-CT04 — Disciplina não pertencente ao professor não aparece nas opções
- **Pré-condição:** Professor autenticado; existe pelo menos uma disciplina cadastrada no sistema que não é de sua responsabilidade
- **Objetivo:** Garantir que o professor só possa indicar monitor para disciplinas sob sua responsabilidade
- **Resultado esperado:** Ao abrir a lista de disciplinas para indicação, a disciplina não pertencente ao professor não é exibida como opção selecionável
- **Tipo:** alternativa
- **Critérios cobertos:** AC3

### US07-CT05 — Indicação de aluno já monitor da mesma disciplina (status já definido)
- **Pré-condição:** Professor autenticado na tela de uma disciplina que lhe é responsável; já existe um vínculo de monitoria para um determinado aluno nessa disciplina (qualquer status)
- **Objetivo:** Verificar comportamento do sistema ao tentar indicar novamente o mesmo aluno como monitor da mesma disciplina
- **Resultado esperado:** Sistema permite a nova indicação ou a rejeita conforme regra de negócio não especificada na user story (a confirmar)
- **Tipo:** a confirmar
- **Critérios cobertos:** a confirmar

### US07-CT06 — Professor sem disciplinas associadas tenta indicar monitor
- **Pré-condição:** Professor autenticado; nenhum registro de disciplina vinculado ao professor no sistema
- **Objetivo:** Verificar o que o sistema exibe quando o professor tenta indicar monitor sem ter disciplinas próprias
- **Resultado esperado:** Sistema informa que não há disciplinas disponíveis para indicação ou apresenta lista vazia (a confirmar)
- **Tipo:** a confirmar
- **Critérios cobertos:** a confirmar