from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from modelledger.api.dependencies import CurrentUser, current_user, get_session, require_role
from modelledger.enums import Role
from modelledger.schemas import ModelCreate, ModelRead, VersionCreate, VersionRead
from modelledger.services.registry import (
    create_model,
    create_version,
    get_model,
    list_models,
    list_versions,
)

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=list[ModelRead])
def read_models(owner: str | None = None, risk_tier: str | None = None, session: Session = Depends(get_session)):
    return list_models(session, owner=owner, risk_tier=risk_tier)


@router.post("", response_model=ModelRead, status_code=status.HTTP_201_CREATED)
def register_model(
    payload: ModelCreate,
    session: Session = Depends(get_session),
    user: CurrentUser = Depends(require_role(Role.SCIENTIST, Role.APPROVER)),
):
    model = create_model(session, payload, user.username)
    session.commit()
    return model


@router.get("/{model_id}", response_model=ModelRead)
def read_model(model_id: str, session: Session = Depends(get_session)):
    model = get_model(session, model_id)
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="model not found")
    return model


@router.get("/{model_id}/versions", response_model=list[VersionRead])
def read_versions(model_id: str, session: Session = Depends(get_session)):
    if get_model(session, model_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="model not found")
    return list_versions(session, model_id)


@router.post("/{model_id}/versions", response_model=VersionRead, status_code=status.HTTP_201_CREATED)
def register_version(
    model_id: str,
    payload: VersionCreate,
    session: Session = Depends(get_session),
    user: CurrentUser = Depends(current_user),
):
    model = get_model(session, model_id)
    if model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="model not found")
    version = create_version(session, model, payload, user.username)
    session.commit()
    return version
