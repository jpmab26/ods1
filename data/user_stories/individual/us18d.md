**Como** monitor, **quero** ver o histórico de atendimentos das minhas monitorias, **para que** eu acompanhe o programa.

**Critérios de Aceitação (para monitor)**

**Cenário 1: Visualização do histórico**
```
Given: monitor autenticado na tela da sua disciplina
When:  visualiza as sessões realizadas
Then:  sistema exibe lista com data, monitor, conteúdo e a quantidade de alunos presentes
```

**Cenário 2: Monitor sem atendimentos registrados**
```
Given: monitor cuja disciplina ainda não tem atendimentos
When:  acessa o histórico
Then:  sistema exibe mensagem de que não há registros
```

**Cenário 3: Monitor só vê sua própria disciplina**
```
Given: monitor tenta acessar histórico de disciplina que não é sua
When:  tenta acessar a rota diretamente
Then:  sistema rejeita com erro de acesso negado
```