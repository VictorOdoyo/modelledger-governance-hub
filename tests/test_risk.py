from modelledger.enums import DriftSeverity, GateState
from modelledger.risk import governance_risk_score, risk_label


def test_governance_risk_score_accumulates_gate_approval_and_drift_signals():
    score = governance_risk_score(GateState.FAILED, pending_approvals=2, latest_drift=DriftSeverity.BREACH, production_deployments=1)
    assert score >= 90
    assert risk_label(score) == "critical"


def test_governance_risk_score_stays_low_for_clean_candidate():
    score = governance_risk_score(GateState.PASSED, pending_approvals=0, latest_drift=DriftSeverity.NONE, production_deployments=0)
    assert score == 10
    assert risk_label(score) == "low"
