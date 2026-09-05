# Architecture

ModelLedger is split into a FastAPI governance API, Celery workers for long-running
evaluation/drift tasks, PostgreSQL for transactional metadata, MinIO-compatible
object storage for model artifacts, optional MLflow integration for experiment
and registry links, and a React operational console.

The API owns decisions. MLflow and MinIO are treated as systems of record for
experiment metadata and binary artifacts, while approval state, gate outcomes,
deployment stages, drift reports, and audit events are persisted in PostgreSQL.

Every workflow records an audit event with actor, subject, action, and compact
payload. Audit rows are append-only in application code.
