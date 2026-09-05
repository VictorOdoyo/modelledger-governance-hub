from modelledger.drift import classify_drift
from modelledger.enums import DriftSeverity


def test_drift_classifier_marks_clean_windows_as_none():
    assert classify_drift({"population_stability_index": 0.04, "accuracy_drop": 0.01}) == DriftSeverity.NONE


def test_drift_classifier_marks_watch_windows():
    assert classify_drift({"population_stability_index": 0.12}) == DriftSeverity.WATCH


def test_drift_classifier_marks_breach_windows():
    assert classify_drift({"population_stability_index": 0.28}) == DriftSeverity.BREACH


def test_drift_classifier_marks_critical_accuracy_drop():
    assert classify_drift({"accuracy_drop": 0.14}) == DriftSeverity.CRITICAL
