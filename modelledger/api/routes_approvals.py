from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from modelledger.api.dependencies import CurrentUser, current_user, get_session, require_role
from modelledger.enums import Role
from modelledger.models import Approval
from modelledger.schemas import ApprovalDecision, ApprovalRead, ApprovalRequestCreate
from modelledger.services.approvals import (
    ApprovalConflict,
    decide_approval,
    list_approvals,
    request_approval,
)
from modelledger.services.registry import get_version

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.get("", response_model=list[ApprovalRead])
def read_approvals(version_id: str | None = None, session: Session = Depends(get_session)):
    return list_approvals(session, version_id)


@router.post("/versions/{version_id}", response_model=ApprovalRead, status_code=status.HTTP_201_CREATED)
def request_version_approval(
    version_id: str,
    payload: ApprovalRequestCreate,
    session: Session = Depends(get_session),
    user: CurrentUser = Depends(current_user),
):
    version = get_version(session, version_id)
    if version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="version not found")
    try:
        approval = request_approval(session, version, payload, user.username)
    except ApprovalConflict as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    session.commit()
    return approval


@router.post("/{approval_id}/approve", response_model=ApprovalRead)
def approve_version(
    approval_id: str,
    payload: ApprovalDecision,
    session: Session = Depends(get_session),
    user: CurrentUser = Depends(require_role(Role.APPROVER)),
):
    approval = session.get(Approval, approval_id)
    if approval is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="approval not found")
    try:
        decided = decide_approval(session, approval, user.username, True, payload.note)
    except ApprovalConflict as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    session.commit()
    return decided


@router.post("/{approval_id}/reject", response_model=ApprovalRead)
def reject_version(
    approval_id: str,
    payload: ApprovalDecision,
    session: Session = Depends(get_session),
    user: CurrentUser = Depends(require_role(Role.APPROVER)),
):
    approval = session.get(Approval, approval_id)
    if approval is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="approval not found")
    try:
        decided = decide_approval(session, approval, user.username, False, payload.note)
    except ApprovalConflict as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    session.commit()
    return decided
