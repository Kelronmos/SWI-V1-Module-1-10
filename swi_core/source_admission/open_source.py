"""Open-source component facade — identity vs licence vs authority vs legal.

Does not claim LEGAL_COMPLIANCE or COPYRIGHT_INFRINGEMENT adjudication.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from swi_core.source_admission.change_control import (
    AdmissionRecord,
    ChangeControlResult,
    ComponentState,
    admit_with_history,
)
from swi_core.source_admission.models import SourceDescriptor


@dataclass(frozen=True)
class OpenSourceComponent:
    component_id: str
    origin: str
    exact_version: str
    content_hash: str
    license_id: Optional[str]
    notice_present: bool = True
    copyright_present: bool = True
    attribution_present: bool = True
    dependency_fingerprint: str = ""
    terms_hash: str = ""
    provenance_verified: bool = False
    privacy_clear: bool = False
    architecture_allowed: bool = False
    target_boundary: str = "SWI_PRIVILEGED_EXECUTION"

    def to_state(self) -> ComponentState:
        desc = SourceDescriptor(
            source_id=self.component_id,
            origin=self.origin,
            version=self.exact_version,
            content_hash=self.content_hash,
            presented_hash=self.content_hash,
            license_id=self.license_id,
            target_boundary=self.target_boundary,
            provenance_verified=self.provenance_verified,
            privacy_clear=self.privacy_clear,
            architecture_allowed=self.architecture_allowed,
        )
        return ComponentState(
            descriptor=desc,
            notice_present=self.notice_present,
            copyright_present=self.copyright_present,
            attribution_present=self.attribution_present,
            dependency_fingerprint=self.dependency_fingerprint,
            terms_hash=self.terms_hash,
        )


def admit_component(
    component: OpenSourceComponent,
    *,
    prior: Optional[AdmissionRecord] = None,
    prior_component: Optional[OpenSourceComponent] = None,
) -> ChangeControlResult:
    prior_state = prior_component.to_state() if prior_component is not None else None
    return admit_with_history(
        component.to_state(),
        prior=prior,
        prior_state=prior_state,
    )
