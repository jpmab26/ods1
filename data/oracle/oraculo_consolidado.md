# Oráculo Consolidado — Casos de Teste Gold Standard

Pipeline: cogerador-testes-monitoria | Revisão: CP3 + reauditoria de evidência (rodada atual)
US no oráculo: US01, US04, US07, US08 (4 das 9 US do backlog; US01/US08 são o
subconjunto de 2 US efetivamente comparado contra o pipeline em `make run-all` — ver
`data/oracle/selecao_us_oraculo.md`; US04/US07 foram adicionadas nesta rodada para
ampliar o oráculo, mas não fazem parte do experimento estatístico já reportado)
Revisores (US01/US08, rodada original): revisor1 + revisor2
Revisores (US04/US07, rodada atual): "revisor A" e "revisor B" simulados por uma
única instância de LLM — **não são revisores humanos independentes reais**; ver
limitação declarada em `data/oracle/selecao_us_oraculo.md`
Limiar de aprovação: soma >= 8 (escala 1/3/5); soma 6 exige consenso; soma <= 4 fica de fora
Total de casos aprovados: 27 (19 em US01/US08 + 3 em US04 + 5 em US07)

**Nota sobre a reauditoria de evidência (rodada anterior):** todos os 19 casos de
US01/US08 tinham o campo `Verificação` citando `backend/tests/*.py`. Isso foi
corrigido — a evidência agora cita exclusivamente código executável
(`backend/**/*.py`, excluindo `tests/`), conforme regra do projeto que proíbe usar a
suíte de testes (escrita às pressas, sem revisão) como fonte de verdade do gold
standard. Nenhum dos 19 casos precisou ser marcado `NAO_VERIFICAVEL` — todos foram
reancorados em código executável com sucesso. O campo `Origem` dos 19 casos de
US01/US08 foi mantido (`manual-revisor1`/`manual-revisor2`) porque reflete a autoria
original do conteúdo do caso — apenas a evidência foi reauditada, não pela mesma via
dos revisores originais.

**Revisão humana final (rodada atual):** os 27 casos foram revisados por um humano
com conhecimento do código do `monitoria-app`, conferindo cada evidência linha a
linha contra `backend/**/*.py` (não-teste). Achado: `US08-CT01` e `US08-CT11`
tinham pré-condição incompleta — não mencionavam que a disciplina da indicação
precisa ter `status = 'ATIVA'` para a aprovação funcionar (`approve_monitoria` faz
um SELECT com JOIN em `disciplinas` exigindo isso antes de qualquer UPDATE; sem essa
condição, a aprovação falha silenciosamente com `NAO_ENCONTRADA`). Ambos corrigidos
diretamente no caso (ver nota "Revisão humana" em cada um). Os demais 25 casos foram
conferidos sem necessidade de correção. Todos os 27 casos estão `Aprovado humano: sim`.

Este arquivo é o **único oráculo canônico** do projeto. Edite aqui para corrigir
casos; o parser em `src/parsers.py` extrai os casos para cálculo de métricas.

---

## US01 — Admin cadastra usuários com perfis

### US01-CT01 — Cadastro bem-sucedido de aluno
- **Pré-condição:** Admin autenticado na tela de gestão de usuários; email 'novo@teste.com' não existe no banco
- **Objetivo:** Verificar que admin consegue criar usuário aluno com status PENDENTE e senha temporária exibida
- **Resultado esperado:** Usuário criado com status PENDENTE; senha temporária exibida ao admin na resposta; flash 'Usuário criado' visível
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: `repository.create_user` insere o registro com `status = 'PENDENTE'` fixo na query SQL (não depende do papel); `service.create_user` retorna `(user_id, temporary_password, None)` repassando a senha gerada por `_generate_temp_password`; `routes.index()` atribui `generated_password` a partir desse retorno e executa `flash("Usuário criado com status PENDENTE.", "success")` quando não há erro — fonte: backend/usuarios/repository.py::create_user; backend/usuarios/service.py::create_user; backend/usuarios/routes.py::index (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US01-CT02 — Cadastro bem-sucedido de professor
- **Pré-condição:** Admin autenticado; email 'prof@teste.com' não existe no banco
- **Objetivo:** Verificar que admin consegue criar usuário professor com status PENDENTE
- **Resultado esperado:** Usuário criado com papel PROFESSOR e status PENDENTE; flash de sucesso exibido
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: `VALID_ROLES = {"ALUNO", "PROFESSOR", "ADMIN"}` inclui 'PROFESSOR'; `create_user` só rejeita papel fora desse conjunto; `repository.create_user` grava o `papel` recebido e `status = 'PENDENTE'` fixo, independente do papel — fonte: backend/usuarios/service.py::create_user (VALID_ROLES); backend/usuarios/repository.py::create_user (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US01-CT03 — Rejeição de email duplicado
- **Pré-condição:** Admin autenticado; usuário com email 'duplicado@teste.com' já existe no banco
- **Objetivo:** Verificar que sistema rejeita cadastro com email já existente e exibe mensagem adequada
- **Resultado esperado:** Sistema retorna mensagem contendo 'ja cadastrado'; nenhum novo usuário criado
- **Tipo:** erro
- **Critérios cobertos:** Cenário 2
- **Verificação:** SUPORTADO — evidência: `if repository.get_user_by_email(normalized_email): return None, None, "Email ja cadastrado"` — a checagem ocorre antes de qualquer INSERT, então nenhum novo registro é criado — fonte: backend/usuarios/service.py::create_user (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US01-CT05 — Rejeição de cadastro sem nome
- **Pré-condição:** Admin autenticado; campo nome enviado vazio
- **Objetivo:** Verificar que sistema rejeita cadastro com nome ausente
- **Resultado esperado:** Sistema retorna mensagem indicando campo obrigatório ausente
- **Tipo:** erro
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: `if not nome or not normalized_email: return None, None, "Nome e email sao obrigatorios."` — nota: o código usa uma única condição combinada para nome OU email ausente, produzindo a mesma mensagem nos dois casos (ver também CT14) — fonte: backend/usuarios/service.py::create_user (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US01-CT06 — Rejeição de papel inválido
- **Pré-condição:** Admin autenticado; campo papel enviado vazio
- **Objetivo:** Verificar que sistema rejeita cadastro com papel não reconhecido
- **Resultado esperado:** Sistema retorna mensagem 'Papel invalido.' ou equivalente
- **Tipo:** erro
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: `role = (papel or "").upper()`; `if role not in VALID_ROLES: return None, None, "Papel invalido."` — string vazia normaliza para "" que não pertence a VALID_ROLES — fonte: backend/usuarios/service.py::create_user (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US01-CT11 — Cadastro de admin cria usuário com status PENDENTE
- **Pré-condição:** Sessão ativa com papel ADMIN; tabela usuarios não contém email 'admin2@teste.com'
- **Objetivo:** Verificar criação de usuário com papel ADMIN e confirmação de status PENDENTE na resposta HTTP
- **Resultado esperado:** POST /usuarios/ retorna HTTP 200 com texto 'PENDENTE' na resposta; registro inserido no banco
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: 'ADMIN' pertence a VALID_ROLES; `repository.create_user` insere com `status = 'PENDENTE'`; `routes.index()` não define status HTTP explícito no POST bem-sucedido (recai no padrão 200 do Flask ao re-renderizar o template) e executa `flash("Usuário criado com status PENDENTE.", "success")`, cujo texto contém 'PENDENTE' — fonte: backend/usuarios/service.py::create_user (VALID_ROLES); backend/usuarios/repository.py::create_user; backend/usuarios/routes.py::index (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US01-CT12 — Senha temporária exibida ao admin após criação
- **Pré-condição:** Admin autenticado; email e nome válidos enviados no formulário de criação
- **Objetivo:** Verificar que a senha temporária gerada é apresentada na interface, não apenas no banco
- **Resultado esperado:** Resposta HTTP 200 contém texto 'Usuário criado' indicando exibição de credenciais
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: `routes.index()` recebe `generated_password` do retorno de `service.create_user` e o repassa a `render_template(..., generated_password=generated_password)`; em caso de sucesso executa `flash("Usuário criado com status PENDENTE.", "success")`, cujo texto contém 'Usuário criado'. Nota: a renderização visual da senha no HTML depende do template em `frontend/templates/`, fora do escopo desta auditoria (restrita a `backend/**/*.py`); a evidência aqui cobre a intenção de exibição no nível de código do backend — fonte: backend/usuarios/routes.py::index (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US01-CT13 — Email duplicado exato rejeitado
- **Pré-condição:** Admin autenticado; 'duplicado@teste.com' já registrado no banco com qualquer papel
- **Objetivo:** Verificar que tentativa de cadastrar o mesmo email uma segunda vez é rejeitada com mensagem específica
- **Resultado esperado:** Resposta com fragmento 'ja cadastrado' (sem acento) na body; nenhum novo registro criado
- **Tipo:** erro
- **Critérios cobertos:** Cenário 2
- **Verificação:** SUPORTADO — evidência: `repository.get_user_by_email` busca por `email = %s` sem diferenciar papel; se encontrado, `service.create_user` retorna a mensagem literal `"Email ja cadastrado"` antes de qualquer INSERT — fonte: backend/usuarios/repository.py::get_user_by_email; backend/usuarios/service.py::create_user (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US01-CT14 — Cadastro sem email rejeitado como campo obrigatório
- **Pré-condição:** Admin autenticado; formulário enviado com campo email vazio
- **Objetivo:** Verificar que email é campo obrigatório na criação de usuário
- **Resultado esperado:** Resposta com mensagem 'obrigatorio' ou 'obrigatório'; usuário não criado
- **Tipo:** erro
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: mesma condição combinada de CT05 — `if not nome or not normalized_email: return None, None, "Nome e email sao obrigatorios."`; email vazio normaliza para string vazia, que é falsy em Python, disparando o mesmo retorno — fonte: backend/usuarios/service.py::create_user (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US01-CT15 — Papel vazio rejeitado como papel inválido
- **Pré-condição:** Admin autenticado; formulário enviado com campo papel em branco
- **Objetivo:** Verificar que papel é validado e string vazia não é aceita
- **Resultado esperado:** Resposta com mensagem 'invalido' ou 'inválido'; usuário não criado
- **Tipo:** borda
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: mesma checagem de CT06 — `(papel or "").upper()` de string vazia resulta em `""`, que não pertence a `VALID_ROLES`, disparando `"Papel invalido."` antes de qualquer INSERT — fonte: backend/usuarios/service.py::create_user (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

---

## US04 — Admin desativa um usuário

### US04-CT01 — Desativação bem-sucedida de usuário ativo
- **Pré-condição:** Admin autenticado; usuário-alvo com id diferente do admin logado existe no banco
- **Objetivo:** Verificar que admin consegue desativar outro usuário e o acesso é revogado
- **Resultado esperado:** Status do usuário-alvo muda para INATIVO no banco; flash 'Usuário desativado com sucesso.' exibido
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: `routes.deactivate(user_id)` chama `service.deactivate_user(user_id)`, que delega a `repository.deactivate_user`, executando `UPDATE usuarios SET status = 'INATIVO' ... WHERE id = %s`; se `rowcount > 0`, a rota executa `flash("Usuário desativado com sucesso.", "success")` — fonte: backend/usuarios/routes.py::deactivate; backend/usuarios/service.py::deactivate_user; backend/usuarios/repository.py::deactivate_user (tipo: código)
- **Origem:** oraculo-llm-simulado
- **Aprovado humano:** sim

### US04-CT02 — Admin não pode desativar o próprio usuário
- **Pré-condição:** Admin autenticado; user_id da URL é igual ao user_id da sessão ativa
- **Objetivo:** Verificar que o sistema impede o admin de desativar sua própria conta
- **Resultado esperado:** Flash 'Você não pode desativar o próprio usuário.' exibido; nenhuma alteração de status no banco (a checagem ocorre antes de chamar o service)
- **Tipo:** borda
- **Critérios cobertos:** Cenário 1 (regra de proteção implícita, não descrita literalmente no texto da US, mas verificada diretamente em código — ver nota de relevância em `selecao_us_oraculo.md`)
- **Verificação:** SUPORTADO — evidência: `routes.deactivate(user_id)` primeiro verifica `if user_id == session.get("user_id")`; em caso positivo, executa `flash("Você não pode desativar o próprio usuário.", "error")` e retorna via redirect **antes** de chamar `service.deactivate_user` — a checagem está em `routes.py`, não em `service.py` — fonte: backend/usuarios/routes.py::deactivate (tipo: código)
- **Origem:** oraculo-llm-simulado
- **Aprovado humano:** sim

### US04-CT03 — Desativar usuário inexistente retorna erro
- **Pré-condição:** Admin autenticado; user_id na URL não corresponde a nenhum registro na tabela usuarios
- **Objetivo:** Verificar tratamento de erro ao tentar desativar um id inexistente
- **Resultado esperado:** Flash 'Usuário não encontrado.' exibido; nenhuma linha afetada no banco
- **Tipo:** erro
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: `repository.deactivate_user` executa o UPDATE e retorna `cursor.rowcount > 0`; se o id não existe, `rowcount == 0`, a função retorna `False`, e `routes.deactivate` executa `flash("Usuário não encontrado.", "error")` no ramo `else` — fonte: backend/usuarios/repository.py::deactivate_user; backend/usuarios/routes.py::deactivate (tipo: código)
- **Origem:** oraculo-llm-simulado
- **Aprovado humano:** sim

---

## US07 — Professor indica aluno como monitor

### US07-CT01 — Indicação bem-sucedida cria vínculo pendente de aprovação
- **Pré-condição:** Professor autenticado; disciplina pertence ao professor (status ATIVA); aluno com papel ALUNO e status ATIVO
- **Objetivo:** Verificar que a indicação cria um registro em `monitorias` com status inicial correto
- **Resultado esperado:** Registro inserido em monitorias com status = 'PENDENTE_APROVACAO'; flash 'Indicação enviada para aprovação.' exibido
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: `routes.indicar()` valida `disciplina_id in allowed_disciplinas` (originada de `disciplinas_service.list_by_professor`) e `aluno_id in allowed_alunos` (originada de `usuarios_repository.list_active_students`); se ambos válidos, chama `service.create_indicacao`, que delega a `repository.create_indicacao`: `INSERT INTO monitorias (...) VALUES (%s, %s, %s, 'PENDENTE_APROVACAO')`; em seguida `flash("Indicação enviada para aprovação.", "success")` — fonte: backend/monitorias/routes.py::indicar; backend/monitorias/repository.py::create_indicacao (tipo: código)
- **Origem:** oraculo-llm-simulado
- **Aprovado humano:** sim

### US07-CT02 — Indicação de aluno inválido é rejeitada
- **Pré-condição:** Professor autenticado; disciplina válida; aluno_id não corresponde a um usuário com papel ALUNO e status ATIVO (ex.: id de um PROFESSOR, ou aluno com status diferente de ATIVO)
- **Objetivo:** Verificar que o sistema rejeita indicação de um id que não é um aluno ativo válido
- **Resultado esperado:** Flash 'Aluno inválido.' exibido; nenhum registro criado em monitorias
- **Tipo:** erro
- **Critérios cobertos:** Cenário 2
- **Verificação:** SUPORTADO (com nota de divergência textual) — evidência: `allowed_alunos` é construído a partir de `usuarios_repository.list_active_students()`, cuja query filtra `papel = 'ALUNO' AND status = 'ATIVO'`; se `aluno_id not in allowed_alunos`, `routes.indicar()` executa `flash("Aluno inválido.", "error")` sem chamar `service.create_indicacao`. Nota: a US descreve a mensagem esperada como "papel inválido", mas o código não valida o papel do usuário isoladamente — ele valida pertencimento a uma lista pré-filtrada por papel E status, e a mensagem exibida é genérica ("Aluno inválido."), não menciona "papel" explicitamente. O comportamento (rejeição) é o mesmo; o texto da mensagem diverge do sugerido na US — fonte: backend/usuarios/repository.py::list_active_students; backend/monitorias/routes.py::indicar (tipo: código)
- **Origem:** oraculo-llm-simulado
- **Aprovado humano:** sim

### US07-CT03 — Disciplina de outro professor não aparece nas opções do formulário
- **Pré-condição:** Professor A autenticado; disciplina X pertence ao professor B
- **Objetivo:** Verificar que o formulário de indicação não lista disciplinas de outros professores
- **Resultado esperado:** GET /monitorias/indicar não inclui a disciplina X entre as opções renderizadas para o professor A
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3
- **Verificação:** SUPORTADO — evidência: `routes.indicar()` popula `disciplinas = disciplinas_service.list_by_professor(professor_id)`, que delega a uma query `WHERE professor_id = %s AND status = 'ATIVA'` — disciplinas de outro professor nunca entram nesse conjunto, logo nunca chegam ao `render_template` como opção — fonte: backend/monitorias/routes.py::indicar; backend/disciplinas/repository.py::list_by_professor (tipo: código)
- **Origem:** oraculo-llm-simulado
- **Aprovado humano:** sim

### US07-CT04 — Tentativa de indicar para disciplina de outro professor via POST forjado é rejeitada
- **Pré-condição:** Professor A autenticado; POST enviado manualmente com disciplina_id pertencente ao professor B
- **Objetivo:** Verificar que a validação server-side também bloqueia a disciplina de outro professor, não apenas a omissão na interface
- **Resultado esperado:** Flash 'Disciplina inválida.' exibido; nenhum registro criado em monitorias
- **Tipo:** borda
- **Critérios cobertos:** Cenário 3 (defesa em profundidade — a US descreve apenas a omissão na interface; este caso cobre a validação equivalente no servidor)
- **Verificação:** SUPORTADO — evidência: `allowed_disciplinas = {d["id"] for d in disciplinas}` é recalculado a cada requisição a partir de `list_by_professor(professor_id)` da sessão atual; `if not disciplina_id or disciplina_id not in allowed_disciplinas: flash("Disciplina inválida.", "error")` — a validação não depende do que foi renderizado no HTML, é refeita no servidor a cada POST — fonte: backend/monitorias/routes.py::indicar (tipo: código)
- **Origem:** oraculo-llm-simulado
- **Aprovado humano:** sim

### US07-CT05 — Indicação com disciplina_id inexistente é rejeitada
- **Pré-condição:** Professor autenticado; disciplina_id enviado não corresponde a nenhuma disciplina no banco
- **Objetivo:** Verificar tratamento de erro para um id de disciplina que não existe
- **Resultado esperado:** Flash 'Disciplina inválida.' exibido; nenhum registro criado em monitorias
- **Tipo:** erro
- **Critérios cobertos:** Cenário 3 (caso de borda derivado do código, aprovado por consenso — ver `selecao_us_oraculo.md`)
- **Verificação:** SUPORTADO — evidência: mesma checagem de CT04 — um disciplina_id que não existe no banco também não pertence a `allowed_disciplinas` (que só contém disciplinas reais do professor autenticado), disparando o mesmo ramo `flash("Disciplina inválida.", "error")` — fonte: backend/monitorias/routes.py::indicar (tipo: código)
- **Origem:** oraculo-llm-simulado
- **Aprovado humano:** sim

---

## US08 — Admin aprova ou rejeita indicação de monitor

### US08-CT01 — Aprovação de indicação pendente muda status para ATIVO
- **Pré-condição:** Admin autenticado; indicação com status PENDENTE_APROVACAO existe no banco, vinculada a uma disciplina com status ATIVA; aluno não possui monitoria ativa
- **Objetivo:** Verificar que admin consegue aprovar indicação e status muda para ATIVO
- **Resultado esperado:** Flash 'indicação aprovada' exibido; status da monitoria no banco = 'ATIVO'
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: `repository.approve_monitoria` primeiro executa um SELECT com JOIN em `disciplinas` exigindo `m.id = %s AND m.status = 'PENDENTE_APROVACAO' AND d.status = 'ATIVA'` (se não encontrar linha, retorna `(False, "NAO_ENCONTRADA")` antes de qualquer UPDATE); só então executa `UPDATE monitorias SET status = 'ATIVO' ... WHERE id = %s AND status = 'PENDENTE_APROVACAO'` e retorna `(True, None)`; `routes.aprovar()` executa `flash("Indicação aprovada.", "success")` nesse caso — fonte: backend/monitorias/repository.py::approve_monitoria; backend/monitorias/routes.py::aprovar (tipo: código)
- **Origem:** manual-revisor1
- **Revisão humana (developer monitoria-app):** pré-condição corrigida — a versão anterior não mencionava que a disciplina precisa ter status ATIVA; sem isso, a aprovação falha silenciosamente com NAO_ENCONTRADA em vez de aprovar, mesmo com a indicação em PENDENTE_APROVACAO. Confirmado em código; caso aprovado após a correção.
- **Aprovado humano:** sim

### US08-CT02 — Rejeição com motivo muda status para REJEITADO
- **Pré-condição:** Admin autenticado; indicação PENDENTE_APROVACAO existe; motivo fornecido
- **Objetivo:** Verificar que admin pode rejeitar indicação com motivo e status muda para REJEITADO
- **Resultado esperado:** Flash 'indicação rejeitada' exibido; status = 'REJEITADO'; motivo_rejeicao salvo no banco
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3
- **Verificação:** SUPORTADO — evidência: `repository.reject_monitoria` executa `UPDATE monitorias SET status = 'REJEITADO', motivo_rejeicao = %s ... WHERE id = %s AND status = 'PENDENTE_APROVACAO'`, retornando `True` se `rowcount > 0`; `routes.rejeitar()` executa `flash("Indicação rejeitada.", "success")` nesse caso — fonte: backend/monitorias/repository.py::reject_monitoria; backend/monitorias/routes.py::rejeitar (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US08-CT03 — Indicação aprovada sai da lista de pendentes
- **Pré-condição:** Admin autenticado; indicação recém-aprovada
- **Objetivo:** Verificar que indicação processada não aparece mais na fila de pendentes
- **Resultado esperado:** GET /monitorias/pendentes não contém a indicação aprovada
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4
- **Verificação:** SUPORTADO — evidência: `repository.list_pending_monitorias` filtra estruturalmente `WHERE m.status = 'PENDENTE_APROVACAO'`; como a aprovação muda o status para 'ATIVO' (ver CT01), a garantia de exclusão da listagem é estática (não depende de execução) — fonte: backend/monitorias/repository.py::list_pending_monitorias; backend/monitorias/repository.py::approve_monitoria (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US08-CT04 — Aprovação bloqueada quando aluno já é monitor ativo
- **Pré-condição:** Admin autenticado; aluno já possui monitoria ATIVO em outra disciplina; nova indicação PENDENTE para segunda disciplina
- **Objetivo:** Verificar que sistema impede aprovação quando aluno já tem monitoria ativa
- **Resultado esperado:** Flash 'já possui monitoria ativa' ou equivalente; indicação permanece PENDENTE_APROVACAO
- **Tipo:** erro
- **Critérios cobertos:** Cenário 2
- **Verificação:** SUPORTADO — evidência: `repository.approve_monitoria` executa `SELECT 1 FROM monitorias WHERE aluno_id = %s AND status = 'ATIVO' AND id <> %s`; se encontrado, retorna `(False, "ALUNO_JA_MONITOR")` sem alterar o status da indicação; `routes.aprovar()` trata esse código com `flash("Aluno já possui monitoria ativa.", "error")` — fonte: backend/monitorias/repository.py::approve_monitoria; backend/monitorias/routes.py::aprovar (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US08-CT05 — Aprovar indicação inexistente retorna erro
- **Pré-condição:** Admin autenticado; ID 999999 não existe na tabela monitorias
- **Objetivo:** Verificar que sistema retorna erro ao tentar aprovar indicação inexistente
- **Resultado esperado:** Flash 'não encontrada' ou equivalente
- **Tipo:** erro
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: `repository.approve_monitoria` retorna `(False, "NAO_ENCONTRADA")` quando o `SELECT` inicial por `id = %s AND status = 'PENDENTE_APROVACAO'` não encontra linha; `routes.aprovar()` cai no ramo `else` e executa `flash("Monitoria não encontrada ou já processada.", "error")`, cujo texto contém 'não encontrada' — fonte: backend/monitorias/repository.py::approve_monitoria; backend/monitorias/routes.py::aprovar (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US08-CT11 — Aprovação de indicação pendente — status ATIVO no banco
- **Pré-condição:** Admin autenticado; monitoria com status PENDENTE_APROVACAO inserida diretamente no banco, vinculada a uma disciplina com status ATIVA; aluno não tem monitoria ativa
- **Objetivo:** Verificar que o campo status na tabela monitorias é alterado para ATIVO após aprovação
- **Resultado esperado:** SELECT status FROM monitorias WHERE id = <id> retorna 'ATIVO'
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: mesma query de CT01 — `UPDATE monitorias SET status = 'ATIVO', atualizado_em = CURRENT_TIMESTAMP WHERE id = %s AND status = 'PENDENTE_APROVACAO'` grava o valor literal 'ATIVO' diretamente no banco (condicionado ao SELECT prévio de existência+disciplina ATIVA, ver CT01) — fonte: backend/monitorias/repository.py::approve_monitoria (tipo: código)
- **Origem:** manual-revisor2
- **Revisão humana (developer monitoria-app):** pré-condição corrigida (mesmo motivo de CT01 — disciplina precisa estar ATIVA). Caso aprovado após a correção.
- **Aprovado humano:** sim

### US08-CT12 — Motivo de rejeição é persistido corretamente no campo motivo_rejeicao
- **Pré-condição:** Admin autenticado; indicação PENDENTE_APROVACAO existe; motivo fornecido no formulário
- **Objetivo:** Verificar que o texto do motivo de rejeição é persistido literalmente no banco
- **Resultado esperado:** Campo motivo_rejeicao na tabela monitorias contém exatamente o texto informado
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3
- **Verificação:** SUPORTADO — evidência: `repository.reject_monitoria(monitoria_id, motivo_rejeicao)` passa `motivo_rejeicao` (ou `None`, se vazio) como parâmetro direto do `UPDATE ... SET motivo_rejeicao = %s`, sem transformação — o valor gravado é exatamente o recebido — fonte: backend/monitorias/repository.py::reject_monitoria (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US08-CT13 — Indicação rejeitada também sai da fila de pendentes
- **Pré-condição:** Admin autenticado; indicação foi rejeitada com motivo
- **Objetivo:** Verificar que indicação rejeitada não aparece mais em GET /monitorias/pendentes
- **Resultado esperado:** Nome do aluno cujas indicação foi rejeitada não aparece na listagem de pendentes
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 4
- **Verificação:** SUPORTADO — evidência: mesma garantia estrutural de CT03 — `list_pending_monitorias` filtra `WHERE m.status = 'PENDENTE_APROVACAO'`, e a rejeição muda o status para 'REJEITADO' (ver CT02), excluindo a indicação da listagem — fonte: backend/monitorias/repository.py::list_pending_monitorias; backend/monitorias/repository.py::reject_monitoria (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US08-CT14 — Tentativa de rejeitar ID inexistente retorna erro
- **Pré-condição:** Admin autenticado; monitoria_id 999999 não existe no banco
- **Objetivo:** Verificar tratamento de rejeição com ID inválido
- **Resultado esperado:** Flash 'não encontrada' ou equivalente; nenhuma alteração no banco
- **Tipo:** erro
- **Critérios cobertos:** Cenário 3
- **Verificação:** SUPORTADO — evidência: `repository.reject_monitoria` executa o `UPDATE ... WHERE id = %s AND status = 'PENDENTE_APROVACAO'`; se `rowcount == 0` (id inexistente), retorna `False`; `routes.rejeitar()` cai no ramo `else` e executa `flash("Monitoria não encontrada ou já processada.", "error")`, cujo texto contém 'não encontrada' — fonte: backend/monitorias/repository.py::reject_monitoria; backend/monitorias/routes.py::rejeitar (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

---
