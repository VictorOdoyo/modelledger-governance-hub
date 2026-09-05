from sqlalchemy import func, select
from sqlalchemy.orm import Session

from modelledger.enums import ApprovalState, DeploymentStage, DriftSeverity, GateState
from modelledger.models import Approval, Deployment, DriftReport, ModelVersion, RegisteredModel


def dashboard_summary(session: Session) -> dict[str, int]:
    models = session.scalar(select(func.count(RegisteredModel.id))) or 0
    versions = session.scalar(select(func.count(ModelVersion.id))) or 0
    failed_gates = session.scalar(
        select(func.count(ModelVersion.id)).where(ModelVersion.gate_state == GateState.FAILED)
    ) or 0
    pending_approvals = session.scalar(
        select(func.count(Approval.id)).where(Approval.state == ApprovalState.REQUESTED)
    ) or 0
    production = session.scalar(
        select(func.count(Deployment.id)).where(Deployment.stage == DeploymentStage.PRODUCTION)
    ) or 0
    drift_breaches = session.scalar(
        select(func.count(DriftReport.id)).where(
            DriftReport.severity.in_([DriftSeverity.BREACH, DriftSeverity.CRITICAL])
        )
    ) or 0
    return {
        "registered_models": models,
        "model_versions": versions,
        "failed_gates": failed_gates,
        "pending_approvals": pending_approvals,
        "production_deployments": production,
        "drift_breaches": drift_breaches,
    }
