### US07-CT01 — Indicação bem-sucedida de aluno válido
- **Pré-condição:** Professor autenticado na tela de uma disciplina de sua responsabilidade; existe aluno com papel "aluno" não vinculado como monitor nessa disciplina
- **Objetivo:** Validar criação de vínculo de monitoria com status inicial correto
- **Resultado esperado:** Sistema cria vínculo com status "Pendente de aprovação" e exibe confirmação
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1

### US07-CT02 — Tentativa de indicação de usuário com papel "professor"
- **Pré-condição:** Professor autenticado na tela de sua disciplina; usuário alvo possui papel "professor" (sem papel "aluno")
- **Objetivo:** Validar rejeição quando usuário indicado não tem papel "aluno"
- **Resultado esperado:** Sistema rejeita a indicação e exibe mensagem de papel inválido
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2

### US07-CT03 — Tentativa de indicação de usuário com papel "admin"
- **Pré-condição:** Professor autenticado na tela de sua disciplina; usuário alvo possui papel "admin" (sem papel "aluno")
- **Objetivo:** Validar rejeição para usuário administrador sem papel discente
- **Resultado esperado:** Sistema rejeita a indicação e exibe mensagem de papel inválido
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2

### US07-CT04 — Tentativa de indicação de usuário sem papel definido
- **Pré-condição:** Professor autenticado na tela de sua disciplina; usuário alvo não possui nenhum papel atribuído
- **Objetivo:** Validar rejeição para usuário sem papel "aluno"
- **Resultado esperado:** Sistema rejeita a indicação e exibe mensagem de papel inválido
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 2

### US07-CT05 — Disciplina de outro professor não listada nas opções
- **Pré-condição:** Professor autenticado; existe disciplina cadastrada sob responsabilidade de outro professor
- **Objetivo:** Validar que disciplinas de outros professores não aparecem para seleção
- **Resultado esperado:** A disciplina de outro professor não é exibida nas opções disponíveis para indicação
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3

### US07-CT06 — Tentativa de indicação via manipulação de ID de disciplina alheia
- **Pré-condição:** Professor autenticado; conhece ID de disciplina de outro professor (ex.: via URL direta ou API)
- **Objetivo:** Validar controle de autorização ao tentar indicar aluno em disciplina não própria
- **Resultado esperado:** Sistema impede a operação e retorna erro de acesso não autorizado ou disciplina não encontrada
- **Tipo:** excepcional
- **Critérios cobertos:** Cenário 3

### US07-CT07 — Indicação de aluno já vinculado como monitor na mesma disciplina
- **Pré-condição:** Professor autenticado na tela de sua disciplina; aluno já possui vínculo ativo ou pendente como monitor nessa disciplina
- **Objetivo:** Validar comportamento ao tentar indicar aluno já monitor da disciplina
- **Resultado esperado:** Sistema impede duplicidade e exibe mensagem de vínculo existente
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US07-CT08 — Indicação de aluno que já é monitor em outra disciplina
- **Pré-condição:** Professor autenticado na tela de sua disciplina; aluno possui vínculo ativo como monitor em disciplina diferente
- **Objetivo:** Validar se sistema permite ou bloqueia aluno monitor em múltiplas disciplinas
- **Resultado esperado:** Sistema permite a nova indicação (ou bloqueia com regra de acúmulo)
- **Tipo:** alternativo
- **Critérios cobertos:** a confirmar

### US07-CT09 — Professor autenticado sem disciplinas cadastradas
- **Pré-condição:** Professor autenticado; não possui nenhuma disciplina sob sua responsabilidade
- **Objetivo:** Validar estado vazio na tela de indicação
- **Resultado esperado:** Sistema exibe mensagem de "Nenhuma disciplina disponível" ou similar; não há opção de indicação
- **Tipo:** excepcional
- **Critérios cobertos:** a confirmar

### US07-CT10 — Indicação com aluno inexistente (ID inválido)
- **Pré-condição:** Professor autenticado na tela de sua disciplina; tenta submeter indicação com ID de aluno que não existe na base
- **Objetivo:** Validar tratamento de referência a usuário inexistente
- **Resultado esperado:** Sistema rejeita com mensagem de aluno não encontrado
- **Tipo:** excepcional
- **Critérios cobertos:** a confirmar