**Como** admin, **quero** editar disciplinas com nome, código e professor, **para que** o programa fique organizado.

**Critérios de Aceitação**

**Cenário 1: Edição bem-sucedida**
```
Given: admin autenticado na tela de gestão de disciplinas
When:  preenche nome, código e seleciona professor responsável e confirma
Then:  disciplina é criada e aparece imediatamente na listagem
```

**Cenário 2: Código duplicado**
```
Given: admin tenta editar uma disciplina com código já existente
When:  confirma o cadastro
Then:  sistema rejeita com mensagem de código duplicado
```

**Cenário 3: Monitor duplicado**
```
Given: admin tenta adicionar um aluno que já é monitor de uma matéria como monitor
When:  confirma o cadastro
Then:  sistema rejeita com mensagem de monitor cadastrado na disciplina <x>
```

**Cenário 4: Professor inválido**
```
Given: admin tenta associar usuário sem papel "professor" como responsável
When:  confirma o cadastro
Then:  sistema rejeita com mensagem de papel inválido
```