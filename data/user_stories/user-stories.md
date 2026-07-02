# [US01] Admin cadastra usuários com perfis
**Épico:** EP01 — Perfis e Autenticação

**Como** admin, **quero** cadastrar usuários com perfis diferentes (aluno, professor e admin), **para que** cada um acesse apenas o que é permitido.

**Critérios BDD:**
```
Given: admin autenticado na tela de gestão de usuários
When:  preenche nome, email e papel e confirma
Then:  usuário é criado com status Pendente e senha temporária exibida ao admin
```
```
Given: admin tenta cadastrar email já existente
When:  confirma o cadastro
Then:  sistema rejeita com mensagem 'Email já cadastrado'
```

# [US02] Usuário faz login com email e senha
**Épico:** EP01 — Perfis e Autenticação

**Como** usuário, **quero** fazer login com email e senha, **para que** eu possa entrar no sistema.

**Critérios BDD:**
```
Given: usuário com status Ativo na tela de login
When:  informa email e senha corretos
Then:  é autenticado e redirecionado para a tela do seu papel
```
```
Given: usuário com status Pendente na tela de login
When:  informa credenciais corretas
Then:  é redirecionado para troca de senha obrigatória
```

# [US03] Monitor edita seu perfil
**Épico:** EP01 — Perfis e Autenticação

**Como** monitor, **quero** editar meu perfil (tipo de contato, contato e horários disponíveis), **para que** meus dados estejam atualizados.

**Critérios de aceitação**

**Cenário 1: Dados não cadastrados**
```
Given: admin ainda não cadastrou dados no seu perfil
When:  acessa perfil
Then:  sistema notifica como pendente para atualizar dados
```

**Cenário 2: Editar perfil**
```
Given: admin autenticado
When:  acessa perfil
Then:  sistema permite editar o tipo de contato, o contato, os horários disponíveis
```

# [US04] Admin desativa um usuário
**Épico:** EP01 — Perfis e Autenticação

**Como** admin, **quero** desativar um usuário, **para que** eu possa remover o acesso de quem saiu do programa.

**Critérios de aceitação:**


**Cenário 1: Desativa usuário ativo**
```
Given: admin autenticado na tela de gestão de usuários
When: clica em desativar usuário
Then: o acesso deste usuário é desativado 
```

**Cenário 2: Usuário já desativado**
```
Given: requisição para desativar usuário já desativado
Then: retorna erro pelo usuário já estar desativado
```

# [US05] Admin muda a senha do usuário manualmente
**Épico:** EP01 — Perfis e Autenticação

**Como** admin, **quero** mudar a senha de um usuário manualmente, **para que** eu consiga desbloquear acesso sem depender de fluxo de email.

**Critérios de aceitação:**

**Cenário 1: Reset bem-sucedido**
```
Given: admin autenticado na tela de gestão de usuários
When:  clica em resetar senha de um usuário
Then:  uma nova senha temporária é gerada e exibida ao admin na tela
       o usuário é marcado com senha_temporaria=True e status PENDENTE
```

**Cenário 2: Usuário inexistente**
```
Given: admin tenta resetar senha de um usuário que não existe
When:  a requisição é processada
Then:  sistema retorna erro 404
```

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

--- 

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

---

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

# [US07] Professor indica aluno como monitor
**Épico:** EP02 — Cadastro de Disciplinas e Monitores

**Como** professor, **quero** indicar um aluno como monitor da minha disciplina, **para que** eu inicie o vínculo de monitoria.

**Critérios de Aceitação**

**Cenário 1: Indicação bem-sucedida**
```
Given: professor autenticado na tela de uma das suas disciplinas
When:  seleciona um aluno e confirma a indicação como monitor
Then:  vínculo é criado com status "Pendente de aprovação"
```

**Cenário 2: Indicação de usuário sem papel aluno**
```
Given: professor tenta indicar usuário que não tem papel "aluno"
When:  confirma a indicação
Then:  sistema rejeita com mensagem de papel inválido
```

**Cenário 3: Disciplina de outro professor**
```
Given: professor autenticado
When:  tenta criar indicação para disciplina que não é de sua responsabilidade
Then:  a disciplina não aparece nas opções disponíveis para ele
```

# [US08] Admin aprova ou rejeita indicação de monitor
**Épico:** EP02 — Cadastro de Disciplinas e Monitores

**Como** admin, **quero** aprovar ou rejeitar indicações de monitor, **para que** eu controle quem entra no programa.

**Critérios de Aceitação**

**Cenário 1: Aprovação de disciplina sem monitor**
```
Given: admin visualiza indicação com status "Pendente de aprovação"
When:  aprova a indicação
Then:  vínculo muda para "Ativo" e o aluno passa a ter acesso como monitor da disciplina
```

**Cenário 2: Aprovação de disciplina com monitor**
```
Given: admin visualiza indicação com status "Pendente de aprovação de alteração de monitor" (uma vez que esta disciplina já tem monitor)
When:  aprova a alteração
Then:  sistema pergunta para confirmar a alteração do monitor antigo pelo novo e, caso aceito, o vínculo muda para "Ativo" e apenas o aluno novo passa a ter acesso como monitor da disciplina
```

**Cenário 3: Rejeição com motivo**
```
Given: admin visualiza indicação com status "Pendente de aprovação"
When:  rejeita informando o motivo
Then:  vínculo muda para "Rejeitado" e o motivo é registrado
```

**Cenário 4: Indicação processada sai da fila**
```
Given: admin aprova ou rejeita uma indicação
When:  retorna à lista de pendentes
Then:  a indicação processada não aparece mais na lista
```

# [US09] Admin lista disciplinas
**Épico:** EP02 — Cadastro de Disciplinas e Monitores

**Como** admin, **quero** listar disciplinas, **para que** eu tenha visibilidade do programa.

**Critérios de Aceitação**

**Cenário 1: Listagem de disciplinas**
```
Given: admin autenticado no painel de disciplinas
When:  acessa a listagem de disciplinas
Then:  sistema exibe por disciplina: código e nome da disciplina, nome do professor, nome do monitor, quantidade de alunos inscritos, status (ativa ou inativa) e horas totais de monitorias. (por padrão aparecem apenas as disciplinas ativas)
```

**Cenário 2: Sem disciplinas ativas**
```
Given: disciplina sem status "Ativo"
When:  admin visualiza a listagem
Then:  sistema exibe mensagem indicando que não há disciplinas ativas
```

# [US10] Aluno vê horários disponíveis de um monitor
**Épico:** EP03 — Agenda e Agendamento

**Como** aluno, **quero** ver os horários disponíveis de um monitor, **para que** agende, por meio de votação quando prefere ser atendido.

**Critérios de Aceitação**

**Cenário 1: Ainda não votou no horário**
```
Given: aluno autenticado na tela da disciplina, vendo os horários disponíveis do monitor
When:  seleciona o horário da monitoria que prefere e confirma
Then:  sistema registra o voto
```

**Cenário 2: Já votou**
```
Given: aluno autenticado na tela da disciplina, vendo os horários disponíveis do monitor com o seu voto registrado
When:  clica em alterar voto, muda o horário e confirma
Then:  sistema altera o voto
```

# [US11] Aluno agenda um horário disponível
**Épico:** EP03 — Agenda e Agendamento

**Como** monitor, **quero** confirmar a monitoria da semana, **para que** eu garanta a sessão semanal.

**Critérios de Aceitação**

**Cenário 1: Metade dos alunos já votaram**
```
Given: admin na seção de monitorias
When:  vê os horários com mais votos da semana e escolhe o horário para confirmar a monitoria semanal
Then:  sistema fecha a votação e deixa a monitoria devidamente agendada
```

**Cenário 2: Metade dos alunos ainda não votaram**
```
Given: admin na seção de monitorias
When:  vê a votação da semana
Then:  sistema retorna "Aguardando votos dos alunos"
```

# [US12] Monitor vê agenda com agendamentos confirmados
**Épico:** EP03 — Agenda e Agendamento

**Como** monitor, **quero** ver minha agenda com agendamentos confirmados, **para que** eu me organize.

**Critérios de Aceitação**

**Cenário 1: Visualização da agenda**
```
Given: monitor autenticado
When:  acessa sua agenda
Then:  visualiza todos os horários criados, diferenciando visualmente os que têm agendamento dos que estão livres
```

**Cenário 2: Dados do agendamento**
```
Given: monitor visualiza horário com agendamento na agenda
When:  acessa o detalhe do agendamento
Then:  sistema exibe nome do aluno, data e horário do atendimento
```

# [US13] Aluno confirma presença ou ausência na motoria
**Épico:** EP03 — Agenda e Agendamento

**Como** aluno, **quero** ser capaz de confirma minha presença ou ausência na monitoria da semana, **para que** o monitor tenha noção de quantas pessoas devem ir à monitoria.

**Critérios de Aceitação**

**Cenário 1: Aluno que vai à monitoria**
```
Given: aluno autenticado com agendamento de monitoria confirmado
When:  confirma a presença
Then:  sistema confirma a presença
```

**Cenário 2: Aluno que não vai à monitoria**
```
Given: aluno autenticado com agendamento de monitoria confirmado
When:  confirma ausência
Then:  sistema não confirma a presença
```

**Cenário 3: Aluno que mudou de ideia**
```
Given: aluno autenticado com agendamento de monitoria confirmado e presença/ausência confirmada
When:  altera a escolha
Then:  sistema atualiza a escolha
```

# [US14] Cancela monitoria agendada
**Épico:** EP03 — Agenda e Agendamento

**Como** monitor, **quero** conseguir cancelar a sessão de monitoria, **para que** caso ocorra um imprevisto a monitoria seja remarcada.

**Critérios de Aceitação**

**Cenário 1: Cancelamento bem-sucedido**
```
Given: monitor autenticado com agendamento confirmado na agenda
When:  solicita o cancelamento com mais de 6 horas de antecedência
Then:  agendamento é removido e a votação da semana é reaberta
```

**Cenário 2: Cancelamento fora do prazo**
```
Given: monitor tenta cancelar agendamento com menos de 6 horas de antecedência
When:  confirma o cancelamento
Then:  sistema rejeita com mensagem "Cancelamento não permitido com menos de 6 horas de antecedência"
```

**Cenário 3: Monitor só cancela agendamentos da sua própria agenda**
```
Given: monitor autenticado
When:  tenta cancelar agendamento de outro monitor
Then:  sistema rejeita com erro de permissão
```

# [US15] Monitor registra presença ou ausência do aluno
**Épico:** EP04 — Registro de Atendimentos e Bolsas

**Como** monitor, **quero** registrar presença ou ausência do aluno, **para que** o histórico de atendimentos seja mantido.

**Critérios de Aceitação**

**Cenário 1: Registro de presença**
```
Given: horário de um agendamento já passou
When:  monitor registra o aluno como "presente"
Then:  registro é salvo no histórico e contabilizado no total de horas do monitor
```

**Cenário 2: Registro de ausência**
```
Given: horário de um agendamento já passou
When:  monitor registra o aluno como "ausente"
Then:  registro é salvo no histórico mas não contabilizado no total de horas
```

**Cenário 3: Registro antes do horário**
```
Given: agendamento com horário ainda no futuro
When:  monitor tenta registrar presença ou ausência
Then:  sistema rejeita com mensagem de que o horário ainda não chegou
```

# [US16] Monitor registra o assunto tratado no atendimento
**Épico:** EP04 — Registro de Atendimentos e Bolsas

**Como** monitor, **quero** registrar o assunto tratado no atendimento, **para que** o que foi coberto fique documentado.

**Critérios de Aceitação**

**Cenário 1: Registro bem-sucedido**
```
Given: monitor na tela de registro de atendimento concluído
When:  preenche o campo de assunto tratado e confirma
Then:  assunto é salvo e exibido no histórico do atendimento
```

**Cenário 2: Campo obrigatório ausente**
```
Given: monitor na tela de registro
When:  tenta confirmar sem preencher o assunto
Then:  sistema impede o envio e aponta o campo faltando
```

# [US17] Admin vê total de horas de monitoria por monitor no mês
**Épico:** EP04 — Registro de Atendimentos e Bolsas

**Como** admin, **quero** ver o total de horas de monitoria por monitor no mês, **para que** eu faça o controle de bolsas.

**Critérios de Aceitação**

**Cenário 1: Painel de horas**
```
Given: admin autenticado no painel de controle de bolsas
When:  acessa o relatório do mês corrente
Then:  sistema exibe total de horas por monitor com destaque para quem está abaixo do limite de 1h semanal
```

**Cenário 2: Filtro por disciplina**
```
Given: admin no painel de horas
When:  filtra por uma disciplina específica
Then:  sistema exibe apenas os monitores vinculados àquela disciplina
```

**Cenário 3: Mês sem atendimentos**
```
Given: admin acessa o painel de um mês sem nenhum atendimento registrado
When:  visualiza o relatório
Then:  sistema exibe lista de monitores com total de horas zerado
```

# [US18] Histórico de monitorias
**Épico:** EP04 — Registro de Atendimentos e Bolsas

---

**Como** admin, **quero** ver o histórico de atendimentos dos monitores de qualquer disciplina, **para que** eu acompanhe o programa.

**Critérios de Aceitação (para admin)**

**Cenário 1: Visualização do histórico**
```
Given: admin autenticado na tela de disciplinas
When:  acessa os detalhes de uma disciplina
Then:  sistema exibe detalhes da disciplina, como: monitor, alunos inscritos, sessões concluídas, horas totais, sessões que pendem ação, alunos inscritos e histórico de monitorias (com data, monitor, conteúdo e a quantidade de alunos presentes)
```
---

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

---

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

---

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

# [US19] Admin gera relatório de participação por disciplina
**Épico:** EP05 — Relatórios e Notificações

**Como** admin, **quero** gerar relatório de participação por disciplina, **para que** eu avalie o impacto do programa.

**Critérios de Aceitação**

**Cenário 1: Geração do relatório**
```
Given: admin seleciona uma disciplina e um intervalo de datas
When:  solicita a geração do relatório
Then:  sistema exibe relatório com total de sessões realizadas, alunos atendidos (únicos), horas realizadas e monitores ativos
```

**Cenário 2: Exportação**
```
Given: admin visualiza relatório gerado
When:  clica em "Exportar CSV"
Then:  arquivo CSV é gerado e disponibilizado para download com sumário e breakdown por monitor
```

**Cenário 3: Disciplina sem atendimentos no período**
```
Given: admin seleciona disciplina e período sem nenhum atendimento registrado
When:  solicita o relatório
Then:  sistema exibe relatório com zeros e mensagem "Nenhum atendimento registrado no período"
```

# [US20] Aluno recebe confirmação quando agendar
**Épico:** EP05 — Relatórios e Notificações

**Como** aluno, **quero** receber confirmação quando agendar, **para que** eu não esqueça o atendimento.

**Critérios de Aceitação**

**Cenário 1: Confirmação após agendamento**
```
Given: aluno que acabou de reservar um horário disponível
When:  o agendamento é confirmado pelo sistema
Then:  aluno vê mensagem de confirmação com data, hora e nome do monitor
```

**Cenário 2: Confirmação persiste na tela de agendamentos**
```
Given: aluno que confirmou um agendamento
When:  acessa a seção "Meus agendamentos" na agenda
Then:  o agendamento aparece listado com data, hora, monitor e local
```

# [US21] Aluno recebe lembrete antes do atendimento
**Épico:** EP05 — Relatórios e Notificações

**Como** aluno, **quero** receber lembrete antes do atendimento, **para que** eu não perca o horário.

**Critérios de aceitação**

**Cenário 1: Lembrete exibido na agenda**
```
Given: aluno com agendamento confirmado nas próximas 24 horas
When:  acessa a tela de agenda
Then:  sistema exibe destaque visual indicando o atendimento próximo com data e hora
```

**Cenário 2: Sem agendamentos próximos**
```
Given: aluno sem agendamentos nas próximas 24 horas
When:  acessa a tela de agenda
Then:  nenhum destaque de lembrete é exibido
```
