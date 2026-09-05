from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from modelledger.models import GateResult, ModelVersion, RegisteredModel
from modelledger.policies import aggregate_gate_state, evaluate_metrics
from modelledger.schemas import EvaluationRequest
from modelledger.services.audit import record_event


def evaluate_version(
    session: Session, model: RegisteredModel, version: ModelVersion, payload: EvaluationRequest, actor: str
) -> list[GateResult]:
    decisions = evaluate_metrics(model.risk_tier, payload.metrics, payload.policy_overrides)
    state = aggregate_gate_state(decisions)
    session.execute(delete(GateResult).where(GateResult.version_id == version.id))
    version.metrics = dict(payload.metrics)
    version.gate_state = state
    results = [
        GateResult(
            version_id=version.id,
            name=decision.name,
            state=decision.state,
            observed=decision.observed,
            threshold=decision.threshold,
            message=decision.message,
        )
        for decision in decisions
    ]
    session.add_all(results)
    record_event(
        session,
        actor=actor,
        action="evaluation.completed",
        subject_type="version",
        subject_id=version.id,
        payload={"gate_state": state.value, "gate_count": len(results)},
    )
    return results


def list_gate_results(session: Session, version_id: str) -> list[GateResult]:
    statement = select(GateResult).where(GateResult.version_id == version_id).order_by(GateResult.name)
    return list(session.scalars(statement).all())
