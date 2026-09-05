from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from modelledger.models import AuditEvent


def record_event(
    session: Session, *, actor: str, action: str, subject_type: str, subject_id: str, payload: dict[str, Any]
) -> AuditEvent:
    event = AuditEvent(
        actor=actor,
        action=action,
        subject_type=subject_type,
        subject_id=subject_id,
        payload=payload,
    )
    session.add(event)
    return event


def list_events(session: Session, subject_type: str | None = None, subject_id: str | None = None) -> list[AuditEvent]:
    statement = select(AuditEvent).order_by(AuditEvent.created_at.desc())
    if subject_type:
        statement = statement.where(AuditEvent.subject_type == subject_type)
    if subject_id:
        statement = statement.where(AuditEvent.subject_id == subject_id)
    return list(session.scalars(statement).all())
