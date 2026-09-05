from modelledger.enums import DriftSeverity, GateState


def governance_risk_score(
    gate_state: GateState,
    pending_approvals: int,
    latest_drift: DriftSeverity,
    production_deployments: int,
) -> int:
    score = 10
    if gate_state == GateState.WARNING:
        score += 18
    elif gate_state == GateState.FAILED:
        score += 38
    score += min(pending_approvals * 8, 24)
    score += {
        DriftSeverity.NONE: 0,
        DriftSeverity.WATCH: 12,
        DriftSeverity.BREACH: 28,
        DriftSeverity.CRITICAL: 42,
    }[latest_drift]
    if production_deployments:
        score += 8
    return min(score, 100)


def risk_label(score: int) -> str:
    if score >= 75:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 30:
        return "medium"
    return "low"
