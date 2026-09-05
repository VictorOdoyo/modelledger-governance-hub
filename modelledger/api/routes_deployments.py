from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from modelledger.api.dependencies import CurrentUser, current_user, get_session
from modelledger.models import Deployment
from modelledger.schemas import DeploymentRead, DeploymentRequest
from modelledger.services.deployments import (
    DeploymentConflict,
    create_deployment,
    list_deployments,
    rollback_deployment,
)
from modelledger.services.registry import get_version

router = APIRouter(prefix="/deployments", tags=["deployments"])


class RollbackRequest(BaseModel):
    reason: str = Field(min_length=8, max_length=1000)


@router.get("", response_model=list[DeploymentRead])
def read_deployments(version_id: str | None = None, session: Session = Depends(get_session)):
    return list_deployments(session, version_id)


@router.post("/versions/{version_id}", response_model=DeploymentRead, status_code=status.HTTP_201_CREATED)
def deploy_version(
    version_id: str,
    payload: DeploymentRequest,
    session: Session = Depends(get_session),
    user: CurrentUser = Depends(current_user),
):
    version = get_version(session, version_id)
    if version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="version not found")
    try:
        deployment = create_deployment(session, version, payload, user.username)
    except DeploymentConflict as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    session.commit()
    return deployment


@router.post("/{deployment_id}/rollback", response_model=DeploymentRead)
def rollback(
    deployment_id: str,
    payload: RollbackRequest,
    session: Session = Depends(get_session),
    user: CurrentUser = Depends(current_user),
):
    deployment = session.get(Deployment, deployment_id)
    if deployment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="deployment not found")
    try:
        rolled_back = rollback_deployment(session, deployment, user.username, payload.reason)
    except DeploymentConflict as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    session.commit()
    return rolled_back
