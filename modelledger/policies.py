from dataclasses import dataclass

from modelledger.enums import GateState, RiskTier
from modelledger.schemas import GateDecision


@dataclass(frozen=True)
class MetricRule:
    name: str
    threshold: float
    direction: str
    warning_margin: float = 0.05

    def evaluate(self, value: float | None) -> GateDecision:
        if value is None:
            return GateDecision(name=self.name, state=GateState.FAILED, message="metric missing")
        if self.direction == "min":
            if value >= self.threshold:
                return GateDecision(
                    name=self.name,
                    state=GateState.PASSED,
                    observed=value,
                    threshold=self.threshold,
                    message="minimum threshold satisfied",
                )
            warning = self.threshold * (1 - self.warning_margin)
            state = GateState.WARNING if value >= warning else GateState.FAILED
        else:
            if value <= self.threshold:
                return GateDecision(
                    name=self.name,
                    state=GateState.PASSED,
                    observed=value,
                    threshold=self.threshold,
                    message="maximum threshold satisfied",
                )
            warning = self.threshold * (1 + self.warning_margin)
            state = GateState.WARNING if value <= warning else GateState.FAILED
        return GateDecision(
            name=self.name,
            state=state,
            observed=value,
            threshold=self.threshold,
            message="outside policy threshold",
        )


DEFAULT_RULES: dict[RiskTier, list[MetricRule]] = {
    RiskTier.LOW: [
        MetricRule("auc", 0.78, "min"),
        MetricRule("latency_ms", 850, "max"),
        MetricRule("data_quality", 0.9, "min"),
    ],
    RiskTier.MEDIUM: [
        MetricRule("auc", 0.82, "min"),
        MetricRule("latency_ms", 650, "max"),
        MetricRule("data_quality", 0.94, "min"),
        MetricRule("bias_gap", 0.12, "max"),
    ],
    RiskTier.HIGH: [
        MetricRule("auc", 0.87, "min"),
        MetricRule("latency_ms", 500, "max"),
        MetricRule("data_quality", 0.97, "min"),
        MetricRule("bias_gap", 0.08, "max"),
    ],
    RiskTier.CRITICAL: [
        MetricRule("auc", 0.9, "min"),
        MetricRule("latency_ms", 400, "max"),
        MetricRule("data_quality", 0.985, "min"),
        MetricRule("bias_gap", 0.05, "max"),
        MetricRule("explainability", 0.8, "min"),
    ],
}


def evaluate_metrics(
    risk_tier: RiskTier, metrics: dict[str, float], overrides: dict[str, float] | None = None
) -> list[GateDecision]:
    override_map = overrides or {}
    rules = [
        MetricRule(rule.name, override_map.get(rule.name, rule.threshold), rule.direction)
        for rule in DEFAULT_RULES[risk_tier]
    ]
    return [rule.evaluate(metrics.get(rule.name)) for rule in rules]


def aggregate_gate_state(decisions: list[GateDecision]) -> GateState:
    if any(decision.state == GateState.FAILED for decision in decisions):
        return GateState.FAILED
    if any(decision.state == GateState.WARNING for decision in decisions):
        return GateState.WARNING
    return GateState.PASSED
