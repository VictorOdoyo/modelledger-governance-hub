from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    APPROVER = "approver"
    SCIENTIST = "scientist"
    VIEWER = "viewer"


class RiskTier(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GateState(StrEnum):
    NOT_RUN = "not_run"
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


class ApprovalState(StrEnum):
    DRAFT = "draft"
    REQUESTED = "requested"
    APPROVED = "approved"
    REJECTED = "rejected"


class DeploymentStage(StrEnum):
    CANDIDATE = "candidate"
    STAGING = "staging"
    PRODUCTION = "production"
    ROLLED_BACK = "rolled_back"


class DriftSeverity(StrEnum):
    NONE = "none"
    WATCH = "watch"
    BREACH = "breach"
    CRITICAL = "critical"
