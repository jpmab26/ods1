**Como** admin, **quero** ver o histórico de atendimentos dos monitores de qualquer disciplina, **para que** eu acompanhe o programa.

**Critérios de Aceitação (para admin)**

**Cenário 1: Visualização do histórico**
```
Given: admin autenticado na tela de disciplinas
When:  acessa os detalhes de uma disciplina
Then:  sistema exibe detalhes da disciplina, como: monitor, alunos inscritos, sessões concluídas, horas totais, sessões que pendem ação, alunos inscritos e histórico de monitorias (com data, monitor, conteúdo e a quantidade de alunos presentes)
```