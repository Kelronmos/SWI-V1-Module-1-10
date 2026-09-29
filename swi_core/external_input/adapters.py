"""Thin adapters: receive, identify, package, forward — never grant authority."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from swi_core.external_input.models import ExternalInput, InputSourceType


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


class APIAdapter:
    def receive(
        self,
        payload: Dict[str, Any],
        *,
        origin: str = "api://demo",
        source_id: str = "api-demo",
        declared_authority: Optional[str] = None,
        requested_action: Optional[str] = None,
        **kwargs: Any,
    ) -> ExternalInput:
        return ExternalInput(
            input_id=_id("api"),
            source_type=InputSourceType.API,
            source_id=source_id,
            origin=origin,
            payload=dict(payload),
            received_at=_now(),
            declared_authority=declared_authority,
            requested_action=requested_action,
            metadata=dict(kwargs),
        )


class AIAppAdapter:
    def receive(
        self,
        payload: Dict[str, Any],
        *,
        origin: str = "ai://demo-model",
        source_id: str = "ai-demo",
        declared_authority: Optional[str] = None,
        requested_action: Optional[str] = None,
        model_id: Optional[str] = None,
        **kwargs: Any,
    ) -> ExternalInput:
        meta = dict(kwargs)
        if model_id:
            meta["model_id"] = model_id
        return ExternalInput(
            input_id=_id("ai"),
            source_type=InputSourceType.AI_APP,
            source_id=source_id,
            origin=origin,
            payload=dict(payload),
            received_at=_now(),
            declared_authority=declared_authority,
            requested_action=requested_action,
            metadata=meta,
        )


class WebhookAdapter:
    def receive(
        self,
        payload: Dict[str, Any],
        *,
        origin: str = "webhook://demo",
        source_id: str = "webhook-demo",
        **kwargs: Any,
    ) -> ExternalInput:
        return ExternalInput(
            input_id=_id("wh"),
            source_type=InputSourceType.WEBHOOK,
            source_id=source_id,
            origin=origin,
            payload=dict(payload),
            received_at=_now(),
            metadata=dict(kwargs),
        )


class SimulationAdapter:
    def receive(
        self,
        payload: Dict[str, Any],
        *,
        origin: str = "sim://demo",
        source_id: str = "sim-demo",
        provenance_verified: bool = True,
        privacy_clear: bool = True,
        architecture_allowed: bool = True,
        **kwargs: Any,
    ) -> ExternalInput:
        return ExternalInput(
            input_id=_id("sim"),
            source_type=InputSourceType.SIMULATION,
            source_id=source_id,
            origin=origin,
            payload=dict(payload),
            received_at=_now(),
            provenance_verified=provenance_verified,
            privacy_clear=privacy_clear,
            architecture_allowed=architecture_allowed,
            metadata=dict(kwargs),
        )
