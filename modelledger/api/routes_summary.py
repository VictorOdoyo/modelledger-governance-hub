from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from modelledger.api.dependencies import get_session
from modelledger.services.summary import dashboard_summary

router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("")
def read_summary(session: Session = Depends(get_session)):
    return dashboard_summary(session)
