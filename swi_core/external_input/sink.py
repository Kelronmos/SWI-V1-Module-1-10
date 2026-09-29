"""Demo execution sink — simulated only; no real-world side effects."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DemoExecutionSink:
    """Records sandbox events only. Never payment/DB/irreversible external I/O."""

    events: List[Dict[str, Any]] = field(default_factory=list)

    def execute(self, input_id: str, action: str | None = None) -> Dict[str, Any]:
        event = {
            "execution_id": f"demo-{len(self.events)+1}",
            "input_id": input_id,
            "action": action or "demo_action",
            "executed": True,
            "side_effects": 1,  # sandbox event count only
            "real_world_side_effects": 0,
            "label": "SIMULATED_ONLY",
        }
        self.events.append(event)
        return event

    def blocked(self, input_id: str, reason: str) -> Dict[str, Any]:
        event = {
            "execution_id": None,
            "input_id": input_id,
            "executed": False,
            "side_effects": 0,
            "real_world_side_effects": 0,
            "reason": reason,
            "label": "BLOCKED",
        }
        self.events.append(event)
        return event
