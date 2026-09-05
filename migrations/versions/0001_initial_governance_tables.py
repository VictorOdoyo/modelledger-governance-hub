"""initial governance tables

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-05
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    role = sa.Enum("ADMIN", "APPROVER", "SCIENTIST", "VIEWER", name="role")
    risk = sa.Enum("LOW", "MEDIUM", "HIGH", "CRITICAL", name="risktier")
    gate = sa.Enum("NOT_RUN", "PASSED", "FAILED", "WARNING", name="gatestate")
    stage = sa.Enum("CANDIDATE", "STAGING", "PRODUCTION", "ROLLED_BACK", name="deploymentstage")
    op.create_table(
        "users",
        sa.Column("username", sa.String(length=80), primary_key=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", role, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "registered_models",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=120), unique=True, nullable=False),
        sa.Column("owner", sa.String(length=120), nullable=False),
        sa.Column("business_domain", sa.String(length=120), nullable=False),
        sa.Column("risk_tier", risk, nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_registered_models_owner", "registered_models", ["owner"])
    op.create_index("ix_registered_models_business_domain", "registered_models", ["business_domain"])
    op.create_table(
        "model_versions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("model_id", sa.String(length=36), sa.ForeignKey("registered_models.id"), nullable=False),
        sa.Column("semantic_version", sa.String(length=80), nullable=False),
        sa.Column("source_run_id", sa.String(length=120), nullable=False),
        sa.Column("artifact_uri", sa.String(length=500), nullable=False),
        sa.Column("training_dataset", sa.String(length=200), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("feature_signature", sa.JSON(), nullable=False),
        sa.Column("stage", stage, nullable=False),
        sa.Column("gate_state", gate, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("model_id", "semantic_version", name="uq_model_version"),
    )
    op.create_index("ix_model_versions_model_id", "model_versions", ["model_id"])
    op.create_index("ix_model_versions_source_run_id", "model_versions", ["source_run_id"])


def downgrade() -> None:
    op.drop_table("model_versions")
    op.drop_table("registered_models")
    op.drop_table("users")
