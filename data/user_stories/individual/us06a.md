# [US06] Admin cadastra e edita disciplinas e alunos
**Épico:** EP02 — Cadastro de Disciplinas e Monitores

**Como** admin, **quero** cadastrar disciplinas com nome, código e professor, **para que** o programa fique organizado.

**Critérios de Aceitação**

**Cenário 1: Cadastro bem-sucedido**
```
Given: admin autenticado na tela de gestão de disciplinas
When:  preenche nome, código e seleciona professor responsável e confirma
Then:  disciplina é criada e aparece imediatamente na listagem
```

**Cenário 2: Código duplicado**
```
Given: admin tenta cadastrar uma disciplina com código já existente
When:  confirma o cadastro
Then:  sistema rejeita com mensagem de código duplicado
```

**Cenário 3: Professor inválido**
```
Given: admin tenta associar usuário sem papel "professor" como responsável
When:  confirma o cadastro
Then:  sistema rejeita com mensagem de papel inválido
```