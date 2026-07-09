"""
Orquestrador do pipeline multiagente (T1/T2/T3).

Estratégia de implementação determinada empiricamente pelo smoke test do
Risco R1 (tests/test_adk_loop_escalation.py, CP2):

  - Estratégia A: SequentialAgent com dois LoopAgent aninhados (forma canônica do ADK).
    Adotada se Echo3 executa normalmente após exit_loop do LoopAgent interno.
  - Estratégia B: BaseAgent customizado com controle de fluxo explícito em Python.
    Adotada se o sinal escalate propagar além do LoopAgent e interromper o SequentialAgent.

Este arquivo implementa a Estratégia A como padrão. Caso o smoke test confirme o
Risco R1, substituir pelo BaseAgent customizado e registrar em outputs/execucao_log.md.

ATENÇÃO: confirmar a API de SequentialAgent e LoopAgent na documentação vigente do ADK
antes de usar (Risco R2, Apêndice C).
"""
from google.adk.agents import SequentialAgent, LoopAgent
from src.agents.a1_gerador import build_a1
from src.agents.a2_critico_cobertura import build_a2
from src.agents.a3_verificador_factual import build_a3
from src.agents.a4_curador import build_a4
from src.config import MAX_ITERATIONS


def build_pipeline_stages() -> list[tuple[str, object]]:
    """Constrói os 4 estágios do pipeline A1 → Loop[A2,A1b] → Loop[A3,A1c] → A4 como
    agentes independentes, cada um o root de sua própria execução (via Runner), em vez de
    um único SequentialAgent atômico.

    Permite a eval/runner.py rodar cada estágio separadamente sobre a MESMA sessão e pular
    estágios já concluídos numa nova tentativa da mesma execução (dentro do mesmo processo)
    — não perde o progresso (e a cota de API já gasta) de estágios anteriores quando um
    estágio posterior falha (ex.: cota diária gratuita esgotada no meio do pipeline).
    Checkpoint é por estágio, não por iteração de loop — uma falha no meio de um LoopAgent
    ainda reinicia aquele loop específico do zero, mas não os estágios já concluídos antes.

    Cada LoopAgent requer uma instância distinta de A1 (ADK impõe parent único
    por instância). A1b e A1c são instâncias independentes com a mesma config.
    """
    a1 = build_a1()
    a1b = build_a1()
    a1c = build_a1()
    a2 = build_a2()
    a3 = build_a3()
    a4 = build_a4()

    # Renomeia para distinguir nas métricas de trace
    a1b.name = "a1_gerador_b"
    a1c.name = "a1_gerador_c"

    loop_cobertura = LoopAgent(
        name="loop_cobertura",
        sub_agents=[a2, a1b],
        max_iterations=MAX_ITERATIONS,
    )

    loop_factual = LoopAgent(
        name="loop_factual",
        sub_agents=[a3, a1c],
        max_iterations=MAX_ITERATIONS,
    )

    return [
        ("a1", a1),
        ("loop_cobertura", loop_cobertura),
        ("loop_factual", loop_factual),
        ("a4", a4),
    ]


def build_pipeline() -> SequentialAgent:
    """Constrói o pipeline A1 → Loop[A2,A1b] → Loop[A3,A1c] → A4 como um único
    SequentialAgent atômico (usado por smoke-adk e testes — sem checkpoint entre estágios;
    para execução real com retomada de progresso, ver build_pipeline_stages() em
    eval/runner.py::_run_multiagent_staged_async)."""
    estagios = build_pipeline_stages()
    return SequentialAgent(
        name="pipeline_cogerador",
        sub_agents=[agente for _, agente in estagios],
    )
