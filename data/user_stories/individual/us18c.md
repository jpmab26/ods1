**Como** professor, **quero** ver o histórico de atendimentos dos monitores da minha disciplina, **para que** eu acompanhe o programa.

**Critérios de Aceitação (para professor)**

**Cenário 1: Visualização do histórico**
```
Given: professor autenticado na tela da sua disciplina
When:  visualiza as sessões realizadas
Then:  sistema exibe lista com data, monitor, conteúdo e a quantidade de alunos presentes
```

**Cenário 2: Professor sem atendimentos registrados**
```
Given: professor cuja disciplina ainda não tem atendimentos
When:  acessa o histórico
Then:  sistema exibe mensagem de que não há registros
```

**Cenário 3: Professor só vê sua própria disciplina**
```
Given: professor tenta acessar histórico de disciplina de outro professor
When:  tenta acessar a rota diretamente
Then:  sistema rejeita com erro de acesso negado
```