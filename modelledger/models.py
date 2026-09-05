from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from modelledger.db import Base
from modelledger.enums import (
    ApprovalState,
    DeploymentStage,
    DriftSeverity,
    GateState,
    RiskTier,
    Role,
)


def now_utc() -> datetime:
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(80), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class RegisteredModel(Base):
    __tablename__ = "registered_models"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    owner: Mapped[str] = mapped_column(String(120), index=True)
    business_domain: Mapped[str] = mapped_column(String(120), index=True)
    risk_tier: Mapped[RiskTier] = mapped_column(Enum(RiskTier), default=RiskTier.MEDIUM)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    versions: Mapped[list["ModelVersion"]] = relationship(back_populates="model")


class ModelVersion(Base):
    __tablename__ = "model_versions"
    __table_args__ = (UniqueConstraint("model_id", "semantic_version", name="uq_model_version"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    model_id: Mapped[str] = mapped_column(ForeignKey("registered_models.id"), index=True)
    semantic_version: Mapped[str] = mapped_column(String(80))
    source_run_id: Mapped[str] = mapped_column(String(120), index=True)
    artifact_uri: Mapped[str] = mapped_column(String(500))
    training_dataset: Mapped[str] = mapped_column(String(200))
    metrics: Mapped[dict[str, float]] = mapped_column(JSON, default=dict)
    feature_signature: Mapped[list[str]] = mapped_column(JSON, default=list)
    stage: Mapped[DeploymentStage] = mapped_column(
        Enum(DeploymentStage), default=DeploymentStage.CANDIDATE
    )
    gate_state: Mapped[GateState] = mapped_column(Enum(GateState), default=GateState.NOT_RUN)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    model: Mapped[RegisteredModel] = relationship(back_populates="versions")


class GateResult(Base):
    __tablename__ = "gate_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    version_id: Mapped[str] = mapped_column(ForeignKey("model_versions.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    state: Mapped[GateState] = mapped_column(Enum(GateState))
    observed: Mapped[float | None]
    threshold: Mapped[float | None]
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    version_id: Mapped[str] = mapped_column(ForeignKey("model_versions.id"), index=True)
    state: Mapped[ApprovalState] = mapped_column(Enum(ApprovalState), default=ApprovalState.REQUESTED)
    requested_by: Mapped[str] = mapped_column(String(80), index=True)
    decided_by: Mapped[str | None] = mapped_column(String(80), nullable=True)
    reason: Mapped[str] = mapped_column(Text)
    decision_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    version_id: Mapped[str] = mapped_column(ForeignKey("model_versions.id"), index=True)
    stage: Mapped[DeploymentStage] = mapped_column(Enum(DeploymentStage), index=True)
    environment: Mapped[str] = mapped_column(String(80), index=True)
    change_ticket: Mapped[str] = mapped_column(String(80), index=True)
    created_by: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    rolled_back_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rollback_reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class DriftReport(Base):
    __tablename__ = "drift_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    version_id: Mapped[str] = mapped_column(ForeignKey("model_versions.id"), index=True)
    severity: Mapped[DriftSeverity] = mapped_column(Enum(DriftSeverity), index=True)
    baseline_window: Mapped[str] = mapped_column(String(80))
    observed_window: Mapped[str] = mapped_column(String(80))
    metrics: Mapped[dict[str, float]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class Artifact(Base):
    __tablename__ = "artifacts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    version_id: Mapped[str] = mapped_column(ForeignKey("model_versions.id"), index=True)
    uri: Mapped[str] = mapped_column(String(500))
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    content_type: Mapped[str] = mapped_column(String(120))
    size_bytes: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    actor: Mapped[str] = mapped_column(String(80), index=True)
    action: Mapped[str] = mapped_column(String(120), index=True)
    subject_type: Mapped[str] = mapped_column(String(80), index=True)
    subject_id: Mapped[str] = mapped_column(String(120), index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
