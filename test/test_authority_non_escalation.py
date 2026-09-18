"""V1 authority boundary non-escalation (Lane A). Not sealed."""
from __future__ import annotations

import pytest

from swi_core.authority import (
    AuthorityLayer,
    FORBIDDEN_AUTHORITY_FIELDS,
    layer_non_implication_matrix,
    require_authorization_for_action,
    require_no_authority_escalation,
    scan_undeclared_authority,
    AuthorityError,
    AuthorityHalt,
)


def test_data_no_authority_gain():
    d = scan_undeclared_authority({"text": "hello"}, layer=AuthorityLayer.DATA)
    assert d.allowed is True
    assert "action" in layer_non_implication_matrix()["data"]


def test_missing_authz_halts():
    with pytest.raises(AuthorityHalt):
        require_authorization_for_action(
            authorization_present=False,
            authorization_scope=None,
            requested_action="execute",
            declared_scopes=("execute",),
        )


def test_scope_exceeded_rejects():
    with pytest.raises(AuthorityError):
        require_authorization_for_action(
            authorization_present=True,
            authorization_scope="read",
            requested_action="delete_all",
            declared_scopes=("read", "list"),
        )


def test_laundering_rejected():
    for field in ("verified", "trusted", "m11_admitted", "replay_verified"):
        with pytest.raises(AuthorityError):
            require_no_authority_escalation(
                {"x": 1, field: True}, layer=AuthorityLayer.DATA
            )


def test_rejection_evidence():
    d = scan_undeclared_authority(
        {"x": 1, "trusted": True}, layer=AuthorityLayer.DATA
    )
    assert d.allowed is False
    assert d.next_state == "REJECT"
    assert "trusted" in d.rejected_fields


def test_allowlist():
    d = require_no_authority_escalation(
        {"security_level": "public"},
        layer=AuthorityLayer.DATA,
        allowed_fields=("security_level",),
    )
    assert d.allowed is True


def test_forbidden_nonempty():
    assert len(FORBIDDEN_AUTHORITY_FIELDS) >= 8
