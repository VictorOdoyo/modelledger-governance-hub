from modelledger.enums import GateState
from modelledger.schemas import EvaluationRequest
from modelledger.services.evaluations import evaluate_version, list_gate_results


def test_evaluation_persists_gate_results_and_updates_version_state(session, seeded):
    model, version = seeded
    results = evaluate_version(
        session,
        model,
        version,
        EvaluationRequest(metrics={"auc": 0.91, "latency_ms": 240, "data_quality": 0.99, "bias_gap": 0.03}),
        actor="scientist",
    )
    session.commit()

    assert len(results) == 4
    assert version.gate_state == GateState.PASSED
    assert len(list_gate_results(session, version.id)) == 4


def test_re_evaluation_replaces_prior_gate_results(session, seeded):
    model, version = seeded
    evaluate_version(session, model, version, EvaluationRequest(metrics={"auc": 0.7}), actor="scientist")
    evaluate_version(
        session,
        model,
        version,
        EvaluationRequest(metrics={"auc": 0.91, "latency_ms": 240, "data_quality": 0.99, "bias_gap": 0.03}),
        actor="scientist",
    )
    session.commit()

    assert len(list_gate_results(session, version.id)) == 4
    assert version.gate_state == GateState.PASSED
