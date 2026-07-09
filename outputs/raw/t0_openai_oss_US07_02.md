### US07-CT01 — Indicação bem‑sucedida de aluno
- **Pré‑condição:** Professor autenticado; disciplina pertence ao professor; aluno cadastrado possui papel “aluno” e ainda não é monitor na disciplina.
- **Objetivo:** Verificar que o professor consegue indicar um aluno como monitor e que o vínculo é criado com status “Pendente de aprovação”.
- **Resultado esperado:** O sistema grava o vínculo monitor‑disciplina com status “Pendente de aprovação” e exibe mensagem de sucesso.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1  

### US07-CT02 — Indicação de usuário sem papel “aluno”
- **Pré‑condição:** Professor autenticado; disciplina pertence ao professor; usuário selecionado possui papel diferente de “aluno” (ex.: “monitor”, “admin” ou nenhum papel).
- **Objetivo:** Garantir que o sistema impede a indicação de usuários que não são alunos.
- **Resultado esperado:** O sistema rejeita a ação e exibe mensagem “Papel inválido” ou equivalente.
- **Tipo:** negativo
- **Critérios cobertos:** Cenário 2  

### US07-CT03 — Disciplina que não pertence ao professor não aparece
- **Pré‑condição:** Professor autenticado; existe disciplina que pertence a outro professor.
- **Objetivo:** Confirmar que disciplinas de responsabilidade de outro professor não são listadas nas opções de indicação.
- **Resultado esperado:** A disciplina de outro professor não está presente na lista de disciplinas disponíveis para seleção.
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3  

### US07-CT04 — Tentativa de indicação com disciplina fora da lista (valor manipulado)
- **Pré‑condição:** Professor autenticado; disciplina não pertence ao professor; tentativa de enviar requisição HTTP com ID de disciplina alheia (por exemplo, via inspeção de HTML).
- **Objetivo:** Verificar se o back‑end valida a propriedade da disciplina independentemente da UI.
- **Resultado esperado:** O servidor responde com erro de autorização (ex.: 403 Forbidden) e não cria vínculo.
- **Tipo:** segurança / negativo
- **Critérios cobertos:** a confirmar (cobertura implícita ao AC3)  

### US07-CT05 — Indicação de aluno já monitor na mesma disciplina
- **Pré‑condição:** Professor autenticado; disciplina pertence ao professor; aluno já possui vínculo como monitor (qualquer status) na mesma disciplina.
- **Objetivo:** Avaliar o comportamento ao tentar criar duplicidade de vínculo.
- **Resultado esperado:** Sistema rejeita a indicação, exibindo mensagem “Aluno já é monitor nesta disciplina” (ou comportamento equivalente).  
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar  

### US07-CT06 — Indicação com campo aluno não selecionado
- **Pré‑condição:** Professor autenticado; disciplina pertence ao professor; tela de indicação aberta.
- **Objetivo:** Verificar validação de campo obrigatório “aluno”.
- **Resultado esperado:** Ao confirmar sem selecionar aluno, o sistema impede o envio e exibe mensagem “Selecione um aluno”.
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar  

### US07-CT07 — Indicação quando professor não está autenticado
- **Pré‑condição:** Usuário não autenticado ou sessão expirada.
- **Objetivo:** Garantir que a funcionalidade só é acessível a professores autenticados.
- **Resultado esperado:** Ao tentar acessar a tela ou enviar a indicação, o sistema redireciona para a página de login ou exibe erro de autorização.
- **Tipo:** segurança / negativo
- **Critérios cobertos:** a confirmar  

### US07-CT08 — Indicação de aluno com status de usuário inativo
- **Pré‑condição:** Professor autenticado; disciplina pertence ao professor; aluno cadastrado tem papel “aluno” porém está marcado como inativo.
- **Objetivo:** Verificar se o sistema impede indicação de alunos inativos.
- **Resultado esperado:** Sistema rejeita a indicação com mensagem “Aluno inativo não pode ser indicado como monitor”.
- **Tipo:** negativo
- **Critérios cobertos:** a confirmar