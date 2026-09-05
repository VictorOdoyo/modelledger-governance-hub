from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from modelledger.api.dependencies import CurrentUser, current_user, get_session
from modelledger.schemas import DriftReportCreate, DriftReportRead
from modelledger.services.drift_reports import create_drift_report, list_drift_reports
from modelledger.services.registry import get_version

router = APIRouter(prefix="/drift", tags=["drift"])


@router.get("", response_model=list[DriftReportRead])
def read_drift_reports(version_id: str | None = None, session: Session = Depends(get_session)):
    return list_drift_reports(session, version_id)


@router.post("/versions/{version_id}", response_model=DriftReportRead, status_code=status.HTTP_201_CREATED)
def report_drift(
    version_id: str,
    payload: DriftReportCreate,
    session: Session = Depends(get_session),
    user: CurrentUser = Depends(current_user),
):
    version = get_version(session, version_id)
    if version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="version not found")
    report = create_drift_report(session, version, payload, user.username)
    session.commit()
    return report
