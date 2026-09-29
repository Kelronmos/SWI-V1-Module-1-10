"""SWI External Input Sandbox — PROTOTYPE / DEMO ONLY.

Open the input surface, not the authority boundary.
External API / AI output = claim data, never automatic authorization.

Status: IMPLEMENTED + TESTED (PROTOTYPE / BOUNDED) when tests pass.
Does not claim production trust, Universal Gate, Seal 5, or compliance.
"""

from swi_core.external_input.adapters import (
    AIAppAdapter,
    APIAdapter,
    SimulationAdapter,
    WebhookAdapter,
)
from swi_core.external_input.gateway import ExternalInputGateway, GatewayResult
from swi_core.external_input.models import ExternalInput, InputSourceType, InputState
from swi_core.external_input.sink import DemoExecutionSink

__all__ = [
    "ExternalInput",
    "InputSourceType",
    "InputState",
    "APIAdapter",
    "AIAppAdapter",
    "WebhookAdapter",
    "SimulationAdapter",
    "ExternalInputGateway",
    "GatewayResult",
    "DemoExecutionSink",
]
