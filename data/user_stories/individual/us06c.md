**Como** admin, **quero** inscrever alunos nas disciplinas **para que** o programa fique organizado.

**Critérios de Aceitação**

**Cenário 1: Adição bem sucedida**
```
Given: admin autenticado na tela de detalhes da disciplina
When:  adiciona alunos por email
Then:  alunos são adicionados na disciplina
```

**Cenário 2: Adição de monitor da monitoria como aluno**
```
Given: admin autenticado na tela de detalhes da disciplina
When:  adiciona o email do monitor desta disciplina
Then:  sistema rejeita com mensagem de "o monitor desta disciplina não pode ser aluno"
```

**Cenário 3: Adição de professor da monitoria como aluno**
```
Given: admin autenticado na tela de detalhes da disciplina
When:  adiciona o email de um professor
Then:  sistema rejeita com mensagem de "professores não podem ser inscritos como aluno"
```

**Cenário 4: Adição de usuário inexistente como aluno**
```
Given: admin autenticado na tela de detalhes da disciplina
When:  adiciona um email inexistente na base de dados
Then:  sistema rejeita com mensagem de "aluno <email> não registrado"
```