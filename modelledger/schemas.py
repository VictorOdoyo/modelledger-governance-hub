from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from modelledger.enums import (
    ApprovalState,
    DeploymentStage,
    DriftSeverity,
    GateState,
    RiskTier,
    Role,
)


class TokenRequest(BaseModel):
    username: str = Field(min_length=2, max_length=80)
    password: str = Field(min_length=8, max_length=120)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Role


class ModelCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    owner: str = Field(min_length=2, max_length=120)
    business_domain: str = Field(min_length=2, max_length=120)
    risk_tier: RiskTier = RiskTier.MEDIUM
    tags: list[str] = Field(default_factory=list, max_length=12)


class ModelRead(ModelCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class VersionCreate(BaseModel):
    semantic_version: str = Field(pattern=r"^\d+\.\d+\.\d+([+-][A-Za-z0-9.-]+)?$")
    source_run_id: str = Field(min_length=3, max_length=120)
    artifact_uri: str = Field(min_length=3, max_length=500)
    training_dataset: str = Field(min_length=2, max_length=200)
    metrics: dict[str, float] = Field(default_factory=dict)
    feature_signature: list[str] = Field(default_factory=list)


class VersionRead(VersionCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    model_id: UUID
    stage: DeploymentStage
    gate_state: GateState
    created_at: datetime


class GateDecision(BaseModel):
    name: str
    state: GateState
    observed: float | None = None
    threshold: float | None = None
    message: str


class EvaluationRequest(BaseModel):
    metrics: dict[str, float]
    policy_overrides: dict[str, float] = Field(default_factory=dict)


class EvaluationRead(BaseModel):
    version_id: UUID
    state: GateState
    decisions: list[GateDecision]


class ApprovalRequestCreate(BaseModel):
    reason: str = Field(min_length=10, max_length=1000)


class ApprovalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    version_id: UUID
    state: ApprovalState
    requested_by: str
    decided_by: str | None
    reason: str
    decision_note: str | None
    created_at: datetime
    decided_at: datetime | None


class ApprovalDecision(BaseModel):
    note: str = Field(min_length=3, max_length=1000)


class DeploymentRequest(BaseModel):
    target_stage: DeploymentStage
    change_ticket: str = Field(min_length=3, max_length=80)
    environment: str = Field(min_length=2, max_length=80)


class DeploymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    version_id: UUID
    stage: DeploymentStage
    environment: str
    change_ticket: str
    created_by: str
    created_at: datetime
    rolled_back_at: datetime | None
    rollback_reason: str | None


class DriftReportCreate(BaseModel):
    baseline_window: str = Field(min_length=3, max_length=80)
    observed_window: str = Field(min_length=3, max_length=80)
    metrics: dict[str, float]


class DriftReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    version_id: UUID
    severity: DriftSeverity
    baseline_window: str
    observed_window: str
    metrics: dict[str, float]
    created_at: datetime


class ArtifactCreate(BaseModel):
    uri: str = Field(min_length=3, max_length=500)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    content_type: str = Field(min_length=3, max_length=120)
    size_bytes: int = Field(ge=1, le=5_000_000_000)


class ArtifactRead(ArtifactCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    version_id: UUID
    created_at: datetime


class AuditRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    actor: str
    action: str
    subject_type: str
    subject_id: str
    payload: dict[str, Any]
    created_at: datetime
