from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from modelledger.api.dependencies import CurrentUser, current_user, get_session
from modelledger.schemas import ArtifactCreate, ArtifactRead
from modelledger.services.artifacts import list_artifacts, register_artifact
from modelledger.services.registry import get_version

router = APIRouter(prefix="/versions/{version_id}/artifacts", tags=["artifacts"])


@router.get("", response_model=list[ArtifactRead])
def read_artifacts(version_id: str, session: Session = Depends(get_session)):
    if get_version(session, version_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="version not found")
    return list_artifacts(session, version_id)


@router.post("", response_model=ArtifactRead, status_code=status.HTTP_201_CREATED)
def add_artifact(
    version_id: str,
    payload: ArtifactCreate,
    session: Session = Depends(get_session),
    user: CurrentUser = Depends(current_user),
):
    version = get_version(session, version_id)
    if version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="version not found")
    artifact = register_artifact(session, version, payload, user.username)
    session.commit()
    return artifact
