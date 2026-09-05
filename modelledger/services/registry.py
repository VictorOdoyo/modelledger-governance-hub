from sqlalchemy import select
from sqlalchemy.orm import Session

from modelledger.models import ModelVersion, RegisteredModel
from modelledger.schemas import ModelCreate, VersionCreate
from modelledger.services.audit import record_event


def create_model(session: Session, payload: ModelCreate, actor: str) -> RegisteredModel:
    model = RegisteredModel(**payload.model_dump())
    session.add(model)
    session.flush()
    record_event(
        session,
        actor=actor,
        action="model.created",
        subject_type="model",
        subject_id=model.id,
        payload={"name": model.name, "risk_tier": model.risk_tier.value},
    )
    return model


def list_models(session: Session, owner: str | None = None, risk_tier: str | None = None) -> list[RegisteredModel]:
    statement = select(RegisteredModel).order_by(RegisteredModel.created_at.desc())
    if owner:
        statement = statement.where(RegisteredModel.owner == owner)
    if risk_tier:
        statement = statement.where(RegisteredModel.risk_tier == risk_tier)
    return list(session.scalars(statement).all())


def get_model(session: Session, model_id: str) -> RegisteredModel | None:
    return session.get(RegisteredModel, model_id)


def create_version(session: Session, model: RegisteredModel, payload: VersionCreate, actor: str) -> ModelVersion:
    version = ModelVersion(model_id=model.id, **payload.model_dump())
    session.add(version)
    session.flush()
    record_event(
        session,
        actor=actor,
        action="version.created",
        subject_type="version",
        subject_id=version.id,
        payload={"model_id": model.id, "semantic_version": version.semantic_version},
    )
    return version


def list_versions(session: Session, model_id: str) -> list[ModelVersion]:
    statement = (
        select(ModelVersion)
        .where(ModelVersion.model_id == model_id)
        .order_by(ModelVersion.created_at.desc())
    )
    return list(session.scalars(statement).all())


def get_version(session: Session, version_id: str) -> ModelVersion | None:
    return session.get(ModelVersion, version_id)
