import pytest

from modelledger.enums import DeploymentStage, GateState
from modelledger.schemas import ApprovalRequestCreate, DeploymentRequest
from modelledger.services.approvals import decide_approval, request_approval
from modelledger.services.deployments import (
    DeploymentConflict,
    create_deployment,
    rollback_deployment,
)


def test_production_deployment_requires_approval(session, seeded):
    _, version = seeded
    with pytest.raises(DeploymentConflict):
        create_deployment(
            session,
            version,
            DeploymentRequest(target_stage=DeploymentStage.PRODUCTION, change_ticket="CHG-100", environment="prod"),
            actor="scientist",
        )


def test_approved_version_can_enter_production(session, seeded):
    _, version = seeded
    version.gate_state = GateState.PASSED
    approval = request_approval(
        session,
        version,
        ApprovalRequestCreate(reason="Ready for controlled production rollout."),
        "scientist",
    )
    decide_approval(session, approval, "approver", True, "Approved")
    deployment = create_deployment(
        session,
        version,
        DeploymentRequest(target_stage=DeploymentStage.PRODUCTION, change_ticket="CHG-101", environment="prod"),
        actor="scientist",
    )
    session.commit()

    assert deployment.stage == DeploymentStage.PRODUCTION
    assert version.stage == DeploymentStage.PRODUCTION


def test_rollback_marks_deployment_and_version(session, seeded):
    _, version = seeded
    deployment = create_deployment(
        session,
        version,
        DeploymentRequest(target_stage=DeploymentStage.STAGING, change_ticket="CHG-102", environment="staging"),
        actor="scientist",
    )
    rollback_deployment(session, deployment, "admin", "metric regression in canary")
    session.commit()

    assert deployment.rolled_back_at is not None
    assert version.stage == DeploymentStage.ROLLED_BACK
