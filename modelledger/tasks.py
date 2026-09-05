from celery import Celery

from modelledger.settings import get_settings

settings = get_settings()
celery_app = Celery(
    "modelledger",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)


@celery_app.task(name="modelledger.evaluate_run")
def evaluate_run(run_id: str, metrics: dict[str, float]) -> dict[str, object]:
    failing = [name for name, value in metrics.items() if name.endswith("_error") and value > 0]
    return {"run_id": run_id, "metrics": metrics, "failing_signals": failing}


@celery_app.task(name="modelledger.generate_drift_report")
def generate_drift_report(version_id: str, metrics: dict[str, float]) -> dict[str, object]:
    from modelledger.drift import classify_drift

    return {"version_id": version_id, "severity": classify_drift(metrics).value}
