from hashlib import sha256

from sqlalchemy import select
from sqlalchemy.orm import Session

from modelledger.models import Artifact, ModelVersion
from modelledger.schemas import ArtifactCreate
from modelledger.services.audit import record_event


def calculate_sha256(data: bytes) -> str:
    return sha256(data).hexdigest()


def register_artifact(session: Session, version: ModelVersion, payload: ArtifactCreate, actor: str) -> Artifact:
    artifact = Artifact(version_id=version.id, **payload.model_dump())
    session.add(artifact)
    session.flush()
    record_event(
        session,
        actor=actor,
        action="artifact.registered",
        subject_type="version",
        subject_id=version.id,
        payload={"artifact_id": artifact.id, "sha256": artifact.sha256},
    )
    return artifact


def list_artifacts(session: Session, version_id: str) -> list[Artifact]:
    statement = select(Artifact).where(Artifact.version_id == version_id).order_by(Artifact.created_at.desc())
    return list(session.scalars(statement).all())
