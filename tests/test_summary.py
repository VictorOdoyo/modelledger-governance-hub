from modelledger.enums import GateState
from modelledger.schemas import ApprovalRequestCreate
from modelledger.services.approvals import request_approval
from modelledger.services.summary import dashboard_summary


def test_dashboard_summary_counts_governance_work(session, seeded):
    _, version = seeded
    version.gate_state = GateState.PASSED
    request_approval(
        session,
        version,
        ApprovalRequestCreate(reason="Independent approval requested for release."),
        "scientist",
    )
    session.commit()

    summary = dashboard_summary(session)

    assert summary["registered_models"] == 1
    assert summary["model_versions"] == 1
    assert summary["pending_approvals"] == 1
