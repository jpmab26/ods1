# Oráculo Consolidado — Casos de Teste Gold Standard

Pipeline: cogerador-testes-monitoria | Revisão: CP3
US no oráculo: US01, US08 (subconjunto de 2 US efetivamente testado em `make run-all`)
Revisores: revisor1 + revisor2 | Limiar de aprovação: soma >= 8 (escala 1/3/5)
Total de casos aprovados: 19

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
- **Verificação:** SUPORTADO — evidência: test_cadastro_aluno_retorna_status_pendente: assert 'PENDENTE' in body; test_cadastro_exibe_senha_temporaria: assert 'Us — fonte: backend/tests/test_us01_cadastro_usuarios.py (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US01-CT02 — Cadastro bem-sucedido de professor
- **Pré-condição:** Admin autenticado; email 'prof@teste.com' não existe no banco
- **Objetivo:** Verificar que admin consegue criar usuário professor com status PENDENTE
- **Resultado esperado:** Usuário criado com papel PROFESSOR e status PENDENTE; flash de sucesso exibido
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: test_cadastro_professor_retorna_status_pendente: assert response.status_code == 200; assert 'PENDENTE' in body — fonte: backend/tests/test_us01_cadastro_usuarios.py (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US01-CT03 — Rejeição de email duplicado
- **Pré-condição:** Admin autenticado; usuário com email 'duplicado@teste.com' já existe no banco
- **Objetivo:** Verificar que sistema rejeita cadastro com email já existente e exibe mensagem adequada
- **Resultado esperado:** Sistema retorna mensagem contendo 'ja cadastrado'; nenhum novo usuário criado
- **Tipo:** erro
- **Critérios cobertos:** Cenário 2
- **Verificação:** SUPORTADO — evidência: test_email_duplicado_rejeitado: assert 'ja cadastrado' in body.lower() — fonte: backend/tests/test_us01_cadastro_usuarios.py (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US01-CT05 — Rejeição de cadastro sem nome
- **Pré-condição:** Admin autenticado; campo nome enviado vazio
- **Objetivo:** Verificar que sistema rejeita cadastro com nome ausente
- **Resultado esperado:** Sistema retorna mensagem indicando campo obrigatório ausente
- **Tipo:** erro
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: test_sem_nome_rejeitado: assert 'obrigatorio' in body.lower() or 'obrigatório' in body.lower() — fonte: backend/tests/test_us01_cadastro_usuarios.py (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US01-CT06 — Rejeição de papel inválido
- **Pré-condição:** Admin autenticado; campo papel enviado vazio
- **Objetivo:** Verificar que sistema rejeita cadastro com papel não reconhecido
- **Resultado esperado:** Sistema retorna mensagem 'Papel invalido.' ou equivalente
- **Tipo:** erro
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: test_sem_papel_rejeitado: assert 'invalido' in body.lower() or 'inválido' in body.lower() — fonte: backend/tests/test_us01_cadastro_usuarios.py (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US01-CT11 — Cadastro de admin cria usuário com status PENDENTE
- **Pré-condição:** Sessão ativa com papel ADMIN; tabela usuarios não contém email 'admin2@teste.com'
- **Objetivo:** Verificar criação de usuário com papel ADMIN e confirmação de status PENDENTE na resposta HTTP
- **Resultado esperado:** POST /usuarios/ retorna HTTP 200 com texto 'PENDENTE' na resposta; registro inserido no banco
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: service.create_user: insere usuario com status='PENDENTE' e senha temporária gerada; rota passa generated_password ao te — fonte: backend/tests/test_us01_cadastro_usuarios.py (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US01-CT12 — Senha temporária exibida ao admin após criação
- **Pré-condição:** Admin autenticado; email e nome válidos enviados no formulário de criação
- **Objetivo:** Verificar que a senha temporária gerada é apresentada na interface, não apenas no banco
- **Resultado esperado:** Resposta HTTP 200 contém texto 'Usuário criado' indicando exibição de credenciais
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: test_cadastro_exibe_senha_temporaria: assert 'Usuário criado' in body — fonte: backend/tests/test_us01_cadastro_usuarios.py (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US01-CT13 — Email duplicado exato rejeitado
- **Pré-condição:** Admin autenticado; 'duplicado@teste.com' já registrado no banco com qualquer papel
- **Objetivo:** Verificar que tentativa de cadastrar o mesmo email uma segunda vez é rejeitada com mensagem específica
- **Resultado esperado:** Resposta com fragmento 'ja cadastrado' (sem acento) na body; nenhum novo registro criado
- **Tipo:** erro
- **Critérios cobertos:** Cenário 2
- **Verificação:** SUPORTADO — evidência: usuarios/service.py mensagem: 'Email ja cadastrado'; test_email_duplicado_rejeitado: assert 'ja cadastrado' in body.lowe — fonte: backend/tests/test_us01_cadastro_usuarios.py (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US01-CT14 — Cadastro sem email rejeitado como campo obrigatório
- **Pré-condição:** Admin autenticado; formulário enviado com campo email vazio
- **Objetivo:** Verificar que email é campo obrigatório na criação de usuário
- **Resultado esperado:** Resposta com mensagem 'obrigatorio' ou 'obrigatório'; usuário não criado
- **Tipo:** erro
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: test_sem_email_rejeitado: assert 'obrigatorio' in body.lower() or 'obrigatório' in body.lower() — fonte: backend/tests/test_us01_cadastro_usuarios.py (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US01-CT15 — Papel vazio rejeitado como papel inválido
- **Pré-condição:** Admin autenticado; formulário enviado com campo papel em branco
- **Objetivo:** Verificar que papel é validado e string vazia não é aceita
- **Resultado esperado:** Resposta com mensagem 'invalido' ou 'inválido'; usuário não criado
- **Tipo:** borda
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: usuarios/service.py mensagem: 'Papel invalido.'; test_sem_papel_rejeitado: assert 'invalido' in body.lower() — fonte: backend/tests/test_us01_cadastro_usuarios.py (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

---

## US08 — Admin aprova ou rejeita indicação de monitor

### US08-CT01 — Aprovação de indicação pendente muda status para ATIVO
- **Pré-condição:** Admin autenticado; indicação com status PENDENTE_APROVACAO existe no banco; aluno não possui monitoria ativa
- **Objetivo:** Verificar que admin consegue aprovar indicação e status muda para ATIVO
- **Resultado esperado:** Flash 'indicação aprovada' exibido; status da monitoria no banco = 'ATIVO'
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: test_admin_aprova_indicacao_pendente: assert 'indicação aprovada' in body.lower(); test_aprovacao_muda_status_para_ativo — fonte: backend/tests/test_us08_aprovar_rejeitar_indicacao.py (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US08-CT02 — Rejeição com motivo muda status para REJEITADO
- **Pré-condição:** Admin autenticado; indicação PENDENTE_APROVACAO existe; motivo fornecido
- **Objetivo:** Verificar que admin pode rejeitar indicação com motivo e status muda para REJEITADO
- **Resultado esperado:** Flash 'indicação rejeitada' exibido; status = 'REJEITADO'; motivo_rejeicao salvo no banco
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3
- **Verificação:** SUPORTADO — evidência: test_rejeicao_muda_status_para_rejeitado: assert state['status'] == 'REJEITADO'; test_motivo_rejeicao_registrado_no_banc — fonte: backend/tests/test_us08_aprovar_rejeitar_indicacao.py (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US08-CT03 — Indicação aprovada sai da lista de pendentes
- **Pré-condição:** Admin autenticado; indicação recém-aprovada
- **Objetivo:** Verificar que indicação processada não aparece mais na fila de pendentes
- **Resultado esperado:** GET /monitorias/pendentes não contém a indicação aprovada
- **Tipo:** principal
- **Critérios cobertos:** Cenário 4
- **Verificação:** SUPORTADO — evidência: test_aprovada_nao_aparece_em_pendentes: assert 'Aluno Fila' not in body; test_rejeitada_nao_aparece_em_pendentes: assert — fonte: backend/tests/test_us08_aprovar_rejeitar_indicacao.py (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US08-CT04 — Aprovação bloqueada quando aluno já é monitor ativo
- **Pré-condição:** Admin autenticado; aluno já possui monitoria ATIVO em outra disciplina; nova indicação PENDENTE para segunda disciplina
- **Objetivo:** Verificar que sistema impede aprovação quando aluno já tem monitoria ativa
- **Resultado esperado:** Flash 'já possui monitoria ativa' ou equivalente; indicação permanece PENDENTE_APROVACAO
- **Tipo:** erro
- **Critérios cobertos:** Cenário 2
- **Verificação:** SUPORTADO — evidência: test_aprovar_aluno_ja_monitor_retorna_erro: assert 'já possui monitoria ativa' in body.lower() or 'ja possui monitoria a — fonte: backend/tests/test_us08_aprovar_rejeitar_indicacao.py (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US08-CT05 — Aprovar indicação inexistente retorna erro
- **Pré-condição:** Admin autenticado; ID 999999 não existe na tabela monitorias
- **Objetivo:** Verificar que sistema retorna erro ao tentar aprovar indicação inexistente
- **Resultado esperado:** Flash 'não encontrada' ou equivalente
- **Tipo:** erro
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: test_aprovar_id_inexistente_retorna_erro: assert 'não encontrada' in body.lower() or 'nao encontrada' in body.lower() — fonte: backend/tests/test_us08_aprovar_rejeitar_indicacao.py (tipo: código)
- **Origem:** manual-revisor1
- **Aprovado humano:** sim

### US08-CT11 — Aprovação de indicação pendente — status ATIVO no banco
- **Pré-condição:** Admin autenticado; monitoria com status PENDENTE_APROVACAO inserida diretamente no banco; aluno não tem monitoria ativa
- **Objetivo:** Verificar que o campo status na tabela monitorias é alterado para ATIVO após aprovação
- **Resultado esperado:** SELECT status FROM monitorias WHERE id = <id> retorna 'ATIVO'
- **Tipo:** principal
- **Critérios cobertos:** Cenário 1
- **Verificação:** SUPORTADO — evidência: test_aprovacao_muda_status_para_ativo: state = _get_monitoria_status(monitoria_id); assert state['status'] == 'ATIVO' — fonte: backend/tests/test_us08_aprovar_rejeitar_indicacao.py (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US08-CT12 — Motivo de rejeição é persistido corretamente no campo motivo_rejeicao
- **Pré-condição:** Admin autenticado; indicação PENDENTE_APROVACAO existe; motivo fornecido no formulário
- **Objetivo:** Verificar que o texto do motivo de rejeição é persistido literalmente no banco
- **Resultado esperado:** Campo motivo_rejeicao na tabela monitorias contém exatamente o texto informado
- **Tipo:** principal
- **Critérios cobertos:** Cenário 3
- **Verificação:** SUPORTADO — evidência: test_motivo_rejeicao_registrado_no_banco: assert state['motivo_rejeicao'] == motivo_esperado — fonte: backend/tests/test_us08_aprovar_rejeitar_indicacao.py (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US08-CT13 — Indicação rejeitada também sai da fila de pendentes
- **Pré-condição:** Admin autenticado; indicação foi rejeitada com motivo
- **Objetivo:** Verificar que indicação rejeitada não aparece mais em GET /monitorias/pendentes
- **Resultado esperado:** Nome do aluno cujas indicação foi rejeitada não aparece na listagem de pendentes
- **Tipo:** alternativo
- **Critérios cobertos:** Cenário 4
- **Verificação:** SUPORTADO — evidência: test_rejeitada_nao_aparece_em_pendentes: assert 'Aluno Fila2' not in body — fonte: backend/tests/test_us08_aprovar_rejeitar_indicacao.py (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

### US08-CT14 — Tentativa de rejeitar ID inexistente retorna erro
- **Pré-condição:** Admin autenticado; monitoria_id 999999 não existe no banco
- **Objetivo:** Verificar tratamento de rejeição com ID inválido
- **Resultado esperado:** Flash 'não encontrada' ou equivalente; nenhuma alteração no banco
- **Tipo:** erro
- **Critérios cobertos:** Cenário 3
- **Verificação:** SUPORTADO — evidência: test_rejeitar_id_inexistente_retorna_erro: assert 'não encontrada' in body.lower() or 'nao encontrada' in body.lower() — fonte: backend/tests/test_us08_aprovar_rejeitar_indicacao.py (tipo: código)
- **Origem:** manual-revisor2
- **Aprovado humano:** sim

---
