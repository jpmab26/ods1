# Seleção das User Stories para o Experimento

## User stories testadas (N=2)

| ID | Título | Épico | Justificativa |
|----|--------|-------|---------------|
| US01 | Admin cadastra usuários | EP01 — Autenticação/gestão de usuários | Validação CRUD + unicidade de email |
| US08 | Admin aprova/rejeita indicação de monitor | EP02 — Gestão de monitores | Máquina de estados com bifurcação (ATIVO/REJEITADO) |

## Critério de seleção

Cobertura de dois épicos centrais do sistema (EP01–EP02), maximizando diversidade
de tipos de regra de negócio (CRUD + unicidade, máquina de estados com bifurcação),
dentro do orçamento de chamadas de API disponível para `make run-all`
(2 US × 2 repetições × 7 tratamentos executados: T0×5 backends + T1 + T2).

## Protocolo de construção do oráculo (casos gold standard)

1. Dois revisores independentes elaboram casos manualmente para cada US
2. Classificação na escala 1/3/5 por ambos (1=irrelevante, 5=cobre diretamente um critério de aceitação)
3. Kappa ponderado linear entre revisores (meta: ≥0,41)
4. Casos com soma 8 ou 10 entram automaticamente no oráculo; soma 6 → consenso entre revisores
5. Cada caso aprovado é ancorado em evidência do código-fonte do `monitoria-app` (campo `Verificação`)

O oráculo final está em `data/oracle/oraculo_consolidado.md` — contém apenas os
19 casos aprovados para US01 e US08 (o subconjunto efetivamente comparado
contra as saídas do pipeline).
