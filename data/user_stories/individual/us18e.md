**Como** aluno, **quero** ver o histórico de atendimentos das minhas monitorias, **para que** eu acompanhe o programa.

**Critérios de Aceitação (para aluno)**

**Cenário 1: Visualização do histórico**
```
Given: aluno autenticado na tela da disciplina que está inscrito
When:  visualiza as sessões realizadas
Then:  sistema exibe lista com data, monitor, conteúdo e se ele estava ou não presente
```

**Cenário 2: Aluno sem monitorias registrados**
```
Given: aluno cuja disciplina ainda não tem atendimentos
When:  acessa o histórico
Then:  sistema exibe mensagem de que não há registros
```

**Cenário 3: Aluno só vê disciplinas que está inscrito**
```
Given: aluno tenta acessar histórico de disciplina que não está inscrito
When:  tenta acessar a rota diretamente
Then:  sistema rejeita com erro de acesso negado
```