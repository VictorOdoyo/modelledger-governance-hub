from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modelledger.api.dependencies import get_session
from modelledger.schemas import AuditRead
from modelledger.services.audit import list_events

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=list[AuditRead])
def read_audit(
    subject_type: str | None = None,
    subject_id: str | None = None,
    session: Session = Depends(get_session),
):
    return list_events(session, subject_type, subject_id)
