### US07-CT01 — Indicação bem‑sucedida de aluno como monitor  
- **Pré‑condição:** Professor autenticado e visualizando a lista de disciplinas que possui; disciplina selecionada pertence ao professor; ao menos um usuário com papel “aluno” está cadastrado na base; o aluno selecionado não possui vínculo de monitoria ativo na mesma disciplina.  
- **Objetivo:** Verificar que a indicação de um aluno para monitoria é criada corretamente.  
- **Resultado esperado:** Após confirmar a indicação, o sistema cria o vínculo de monitoria com status “Pendente de aprovação” e exibe mensagem de sucesso.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 1 – Indicação bem‑sucedida  

### US07-CT02 — Tentativa de indicação de usuário sem papel “aluno”  
- **Pré‑condição:** Professor autenticado; disciplina seleção válida; usuário selecionado possui papel diferente de “aluno” (ex.: “colaborador”, “admin”).  
- **Objetivo:** Garantir que o sistema impede a indicação de usuários que não são alunos.  
- **Resultado esperado:** Ao confirmar a indicação, o sistema rejeita a operação e exibe a mensagem “Papel inválido: o usuário não é aluno”.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 2 – Indicação de usuário sem papel aluno  

### US07-CT03 — Disciplina não pertence ao professor logado  
- **Pré‑condição:** Professor autenticado; existe disciplina cadastrada que pertence a outro professor.  
- **Objetivo:** Assegurar que disciplinas que não são de responsabilidade do professor não são apresentadas para indicação.  
- **Resultado esperado:** Na tela de escolha de disciplinas, a disciplina de outro professor não aparece na lista; o professor não pode iniciar a indicação para ela.  
- **Tipo:** principal  
- **Critérios cobertos:** Cenário 3 – Disciplina de outro professor  

### US07-CT04 — Professor tenta indicar aluno sem selecionar nenhum usuário  
- **Pré‑condição:** Professor autenticado; disciplina válida selecionada; lista de alunos exibida, porém nenhuma linha está marcada.  
- **Objetivo:** Verificar o tratamento de tentativa de confirmação sem que um aluno seja escolhido.  
- **Resultado esperado:** Sistema impede a confirmação e exibe mensagem “Selecione um aluno para indicar”.  
- **Tipo:** alternativo  
- **Critérios cobertos:** a confirmar (comportamento esperado não explicitado nos AC)  

### US07-CT05 — Indicação de aluno já com vínculo “Pendente de aprovação” na mesma disciplina  
- **Pré‑condição:** Professor autenticado; disciplina válida; aluno já possui vínculo de monitoria com status “Pendente de aprovação” para aquela disciplina.  
- **Objetivo:** Garantir que o sistema impede a criação de vínculo duplicado.  
- **Resultado esperado:** Ao confirmar a nova indicação, o sistema rejeita e informa “Aluno já indicado como monitor para esta disciplina”.  
- **Tipo:** alternativo  
- **Critérios cobertos:** a confirmar (regra de unicidade não descrita nos AC)  

### US07-CT06 — Indicação de aluno já aprovado como monitor na disciplina  
- **Pré‑condição:** Professor autenticado; disciplina válida; aluno já possui vínculo de monitoria com status “Aprovado” na mesma disciplina.  
- **Objetivo:** Verificar que o sistema impede re‑indicação de monitor já aprovado.  
- **Resultado esperado:** Sistema bloqueia a operação e exibe mensagem “Aluno já é monitor desta disciplina”.  
- **Tipo:** alternativo  
- **Critérios cobertos:** a confirmar (não especificado nos AC)  

### US07-CT07 — Falha de comunicação com o banco ao salvar vínculo  
- **Pré‑condição:** Professor autenticado; disciplina válida; aluno elegível selecionado; simulação de erro de conexão/comando SQL ao inserir o vínculo.  
- **Objetivo:** Avaliar o tratamento de erro interno durante a criação do vínculo.  
- **Resultado esperado:** Sistema captura a exceção, não cria o vínculo, e apresenta mensagem genérica de erro “Não foi possível registrar a indicação. Tente novamente mais tarde”.  
- **Tipo:** alternativo  
- **Critérios cobertos:** a confirmar (comportamento de falha de infraestrutura não está nos AC)