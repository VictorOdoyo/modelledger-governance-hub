from modelledger.enums import GateState, RiskTier
from modelledger.policies import aggregate_gate_state, evaluate_metrics


def test_high_risk_policy_requires_quality_bias_and_latency():
    decisions = evaluate_metrics(
        RiskTier.HIGH,
        {"auc": 0.9, "latency_ms": 425, "data_quality": 0.99, "bias_gap": 0.04},
    )
    assert aggregate_gate_state(decisions) == GateState.PASSED


def test_missing_metric_fails_policy_gate():
    decisions = evaluate_metrics(RiskTier.CRITICAL, {"auc": 0.93})
    failed = {decision.name for decision in decisions if decision.state == GateState.FAILED}
    assert {"latency_ms", "data_quality", "bias_gap", "explainability"} <= failed


def test_threshold_overrides_are_honored():
    decisions = evaluate_metrics(RiskTier.MEDIUM, {"auc": 0.84}, {"auc": 0.86})
    auc = next(decision for decision in decisions if decision.name == "auc")
    assert auc.threshold == 0.86
    assert auc.state == GateState.WARNING
