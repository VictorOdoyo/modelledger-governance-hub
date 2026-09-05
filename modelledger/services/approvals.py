from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from modelledger.enums import ApprovalState, GateState
from modelledger.models import Approval, ModelVersion
from modelledger.schemas import ApprovalRequestCreate
from modelledger.services.audit import record_event


class ApprovalConflict(ValueError):
    pass


def request_approval(session: Session, version: ModelVersion, payload: ApprovalRequestCreate, actor: str) -> Approval:
    if version.gate_state == GateState.FAILED:
        raise ApprovalConflict("failed evaluation gates cannot be sent for approval")
    approval = Approval(version_id=version.id, requested_by=actor, reason=payload.reason)
    session.add(approval)
    session.flush()
    record_event(
        session,
        actor=actor,
        action="approval.requested",
        subject_type="version",
        subject_id=version.id,
        payload={"approval_id": approval.id},
    )
    return approval


def decide_approval(session: Session, approval: Approval, actor: str, approved: bool, note: str) -> Approval:
    if approval.state != ApprovalState.REQUESTED:
        raise ApprovalConflict("approval is already decided")
    if approval.requested_by == actor:
        raise ApprovalConflict("requester cannot approve their own model version")
    approval.state = ApprovalState.APPROVED if approved else ApprovalState.REJECTED
    approval.decided_by = actor
    approval.decision_note = note
    approval.decided_at = datetime.now(UTC)
    record_event(
        session,
        actor=actor,
        action="approval.approved" if approved else "approval.rejected",
        subject_type="approval",
        subject_id=approval.id,
        payload={"version_id": approval.version_id},
    )
    return approval


def latest_approved_approval(session: Session, version_id: str) -> Approval | None:
    statement = (
        select(Approval)
        .where(Approval.version_id == version_id, Approval.state == ApprovalState.APPROVED)
        .order_by(Approval.decided_at.desc())
    )
    return session.scalars(statement).first()


def list_approvals(session: Session, version_id: str | None = None) -> list[Approval]:
    statement = select(Approval).order_by(Approval.created_at.desc())
    if version_id:
        statement = statement.where(Approval.version_id == version_id)
    return list(session.scalars(statement).all())
