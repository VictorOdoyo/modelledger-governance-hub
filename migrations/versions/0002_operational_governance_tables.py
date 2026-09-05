"""operational governance tables

Revision ID: 0002_operational
Revises: 0001_initial
Create Date: 2026-09-05
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_operational"
down_revision: str | None = "0001_initial"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "gate_results",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), sa.ForeignKey("model_versions.id"), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("state", sa.String(length=20), nullable=False),
        sa.Column("observed", sa.Float(), nullable=True),
        sa.Column("threshold", sa.Float(), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "approvals",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), sa.ForeignKey("model_versions.id"), nullable=False),
        sa.Column("state", sa.String(length=20), nullable=False),
        sa.Column("requested_by", sa.String(length=80), nullable=False),
        sa.Column("decided_by", sa.String(length=80), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("decision_note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        "deployments",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), sa.ForeignKey("model_versions.id"), nullable=False),
        sa.Column("stage", sa.String(length=40), nullable=False),
        sa.Column("environment", sa.String(length=80), nullable=False),
        sa.Column("change_ticket", sa.String(length=80), nullable=False),
        sa.Column("created_by", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("rolled_back_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rollback_reason", sa.Text(), nullable=True),
    )
    op.create_table(
        "drift_reports",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), sa.ForeignKey("model_versions.id"), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("baseline_window", sa.String(length=80), nullable=False),
        sa.Column("observed_window", sa.String(length=80), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "artifacts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("version_id", sa.String(length=36), sa.ForeignKey("model_versions.id"), nullable=False),
        sa.Column("uri", sa.String(length=500), nullable=False),
        sa.Column("sha256", sa.String(length=64), nullable=False),
        sa.Column("content_type", sa.String(length=120), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("actor", sa.String(length=80), nullable=False),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("subject_type", sa.String(length=80), nullable=False),
        sa.Column("subject_id", sa.String(length=120), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("artifacts")
    op.drop_table("drift_reports")
    op.drop_table("deployments")
    op.drop_table("approvals")
    op.drop_table("gate_results")
