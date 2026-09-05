import pytest

from modelledger.enums import ApprovalState, GateState
from modelledger.schemas import ApprovalRequestCreate
from modelledger.services.approvals import ApprovalConflict, decide_approval, request_approval


def test_failed_gate_version_cannot_request_approval(session, seeded):
    _, version = seeded
    version.gate_state = GateState.FAILED

    with pytest.raises(ApprovalConflict):
        request_approval(session, version, ApprovalRequestCreate(reason="Need approval for rollout"), "scientist")


def test_requester_cannot_approve_own_request(session, seeded):
    _, version = seeded
    version.gate_state = GateState.PASSED
    approval = request_approval(
        session,
        version,
        ApprovalRequestCreate(reason="Governance package is ready for review."),
        "scientist",
    )

    with pytest.raises(ApprovalConflict):
        decide_approval(session, approval, "scientist", True, "looks fine")


def test_independent_approval_records_decision_actor(session, seeded):
    _, version = seeded
    version.gate_state = GateState.PASSED
    approval = request_approval(
        session,
        version,
        ApprovalRequestCreate(reason="Governance package is ready for review."),
        "scientist",
    )
    decide_approval(session, approval, "approver", True, "Approved for staging")
    session.commit()

    assert approval.state == ApprovalState.APPROVED
    assert approval.decided_by == "approver"
