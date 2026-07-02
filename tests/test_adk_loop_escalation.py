"""
Smoke test do Risco R1 (Apêndice C): valida empiricamente se o sinal escalate=True
de um LoopAgent propaga além e interrompe o SequentialAgent pai.

Usa BaseAgent customizados em vez de LlmAgent+DryRunModel para testar a arquitetura
do runtime do ADK sem dependência de chamadas de modelo.

Resultado esperado (baseado em análise do código-fonte do ADK 2.3.0):
  - LoopAgent lê event.actions.escalate e encerra seu laço interno.
  - SequentialAgent NÃO verifica escalate (apenas should_pause_invocation, que
    responde a long-running tools); portanto Echo3 DEVE executar.
  - Se Echo3 NÃO executar, Risco R1 se confirma e pipeline.py deve adotar
    Estratégia B (BaseAgent customizado).

Resultado observado documentado em outputs/execucao_log.md (CP2).
"""
from __future__ import annotations

import asyncio
from typing import AsyncGenerator

import pytest

pytest.importorskip("google.adk", reason="google-adk não instalado")


from google.adk.agents import LoopAgent, SequentialAgent
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.events.event_actions import EventActions
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import google.genai.types as genai_types


class EchoAgent(BaseAgent):
    """Agente mínimo: registra execução via state_delta e emite evento de texto."""

    tag: str

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        content = genai_types.Content(
            parts=[genai_types.Part(text=f"[{self.tag}] ok")],
            role="model",
        )
        yield Event(
            invocation_id=ctx.invocation_id,
            author=self.name,
            content=content,
            actions=EventActions(state_delta={f"ran_{self.tag}": True}),
        )


class ExitAgent(BaseAgent):
    """Agente mínimo: emite evento com escalate=True para encerrar o LoopAgent pai."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        yield Event(
            invocation_id=ctx.invocation_id,
            author=self.name,
            actions=EventActions(
                escalate=True,
                skip_summarization=True,
                state_delta={"ran_exit_agent": True},
            ),
        )


@pytest.mark.asyncio
async def test_loop_escalation_does_not_propagate_to_sequential():
    """
    Estrutura: SequentialAgent([Echo1, LoopAgent([ExitAgent]), Echo3])

    Echo1 roda → LoopAgent inicia → ExitAgent emite escalate → LoopAgent
    encerra o laço → SequentialAgent continua → Echo3 roda.

    Falha se Echo3 NÃO rodar (Risco R1 confirmado).
    """
    session_service = InMemorySessionService()

    echo1 = EchoAgent(name="echo1", tag="echo1")
    exit_ag = ExitAgent(name="exit_agent")
    echo3 = EchoAgent(name="echo3", tag="echo3")

    loop_inner = LoopAgent(name="loop_inner", sub_agents=[exit_ag], max_iterations=3)
    pipeline = SequentialAgent(
        name="pipeline_risco_r1",
        sub_agents=[echo1, loop_inner, echo3],
    )

    runner = Runner(
        agent=pipeline,
        app_name="risco_r1_test",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="risco_r1_test",
        user_id="tester",
    )

    user_msg = genai_types.Content(
        parts=[genai_types.Part(text="smoke test")],
        role="user",
    )

    async for _ in runner.run_async(
        user_id="tester",
        session_id=session.id,
        new_message=user_msg,
    ):
        pass

    session = await session_service.get_session(
        app_name="risco_r1_test",
        user_id="tester",
        session_id=session.id,
    )

    assert session.state.get("ran_echo1"), "Echo1 não executou"
    assert session.state.get("ran_exit_agent"), "ExitAgent não executou"
    assert session.state.get("ran_echo3"), (
        "Risco R1 CONFIRMADO: Echo3 não executou após LoopAgent encerrar. "
        "Pipeline deve migrar para Estratégia B (BaseAgent customizado)."
    )
