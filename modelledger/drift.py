from modelledger.enums import DriftSeverity


def classify_drift(metrics: dict[str, float]) -> DriftSeverity:
    population = metrics.get("population_stability_index", 0)
    accuracy_drop = metrics.get("accuracy_drop", 0)
    volume_shift = metrics.get("volume_shift", 0)
    if population >= 0.4 or accuracy_drop >= 0.12:
        return DriftSeverity.CRITICAL
    if population >= 0.25 or accuracy_drop >= 0.08 or volume_shift >= 0.35:
        return DriftSeverity.BREACH
    if population >= 0.1 or accuracy_drop >= 0.03 or volume_shift >= 0.18:
        return DriftSeverity.WATCH
    return DriftSeverity.NONE
