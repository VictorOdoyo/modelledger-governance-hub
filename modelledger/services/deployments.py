from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from modelledger.enums import DeploymentStage
from modelledger.models import Deployment, ModelVersion
from modelledger.schemas import DeploymentRequest
from modelledger.services.approvals import latest_approved_approval
from modelledger.services.audit import record_event


class DeploymentConflict(ValueError):
    pass


def create_deployment(session: Session, version: ModelVersion, payload: DeploymentRequest, actor: str) -> Deployment:
    if payload.target_stage == DeploymentStage.PRODUCTION and latest_approved_approval(session, version.id) is None:
        raise DeploymentConflict("production deployment requires an independent approval")
    version.stage = payload.target_stage
    deployment = Deployment(
        version_id=version.id,
        stage=payload.target_stage,
        environment=payload.environment,
        change_ticket=payload.change_ticket,
        created_by=actor,
    )
    session.add(deployment)
    session.flush()
    record_event(
        session,
        actor=actor,
        action="deployment.created",
        subject_type="deployment",
        subject_id=deployment.id,
        payload={"version_id": version.id, "stage": deployment.stage.value},
    )
    return deployment


def rollback_deployment(session: Session, deployment: Deployment, actor: str, reason: str) -> Deployment:
    if deployment.rolled_back_at is not None:
        raise DeploymentConflict("deployment already rolled back")
    deployment.rolled_back_at = datetime.now(UTC)
    deployment.rollback_reason = reason
    version = session.get(ModelVersion, deployment.version_id)
    if version:
        version.stage = DeploymentStage.ROLLED_BACK
    record_event(
        session,
        actor=actor,
        action="deployment.rolled_back",
        subject_type="deployment",
        subject_id=deployment.id,
        payload={"reason": reason},
    )
    return deployment


def list_deployments(session: Session, version_id: str | None = None) -> list[Deployment]:
    statement = select(Deployment).order_by(Deployment.created_at.desc())
    if version_id:
        statement = statement.where(Deployment.version_id == version_id)
    return list(session.scalars(statement).all())
