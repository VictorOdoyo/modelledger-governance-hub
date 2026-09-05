from sqlalchemy import select
from sqlalchemy.orm import Session

from modelledger.drift import classify_drift
from modelledger.models import DriftReport, ModelVersion
from modelledger.schemas import DriftReportCreate
from modelledger.services.audit import record_event


def create_drift_report(
    session: Session, version: ModelVersion, payload: DriftReportCreate, actor: str
) -> DriftReport:
    severity = classify_drift(payload.metrics)
    report = DriftReport(
        version_id=version.id,
        severity=severity,
        baseline_window=payload.baseline_window,
        observed_window=payload.observed_window,
        metrics=payload.metrics,
    )
    session.add(report)
    session.flush()
    record_event(
        session,
        actor=actor,
        action="drift.reported",
        subject_type="version",
        subject_id=version.id,
        payload={"severity": severity.value},
    )
    return report


def list_drift_reports(session: Session, version_id: str | None = None) -> list[DriftReport]:
    statement = select(DriftReport).order_by(DriftReport.created_at.desc())
    if version_id:
        statement = statement.where(DriftReport.version_id == version_id)
    return list(session.scalars(statement).all())
