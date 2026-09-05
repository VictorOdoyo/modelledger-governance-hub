# ModelLedger Governance Hub

ModelLedger is a production-oriented model governance platform for registering
machine-learning models, tracking versions, evaluating release gates, requesting
independent approvals, staging deployments, recording rollback decisions, and
watching drift reports.

The project is intentionally runnable without paid infrastructure. Local
development can use SQLite, while Docker Compose provides PostgreSQL, Redis,
MinIO-compatible object storage, the FastAPI API, a Celery worker, and the React
governance console.

## Features

- Versioned FastAPI API with OpenAPI documentation.
- Registered model and model-version workflows.
- Risk-tiered evaluation policies for accuracy, latency, data quality, bias, and explainability.
- Approval workflow with maker-checker enforcement.
- Production deployment records that require independent approval.
- Rollback records that preserve immutable deployment history.
- Drift reports with severity classification.
- Artifact metadata with SHA-256 validation.
- Audit trail for model, version, evaluation, approval, deployment, drift, and artifact actions.
- Prometheus metrics endpoint.
- Optional MLflow registry adapter.
- MinIO/S3 presigned upload adapter.
- Celery tasks for asynchronous evaluation and drift work.
- React + TypeScript console for registry, gates, approvals, drift, deployments, experiments, and rollback planning.
- Backend unit, API, and optional PostgreSQL integration tests.
- Frontend selector tests and production build verification.
- GitHub Actions CI for backend, frontend, and container builds.

## Stack

- Python 3.13, FastAPI, SQLAlchemy, Pydantic Settings, PyJWT, Celery
- PostgreSQL, Redis, MinIO-compatible S3 storage
- Optional MLflow integration through `mlflow-skinny`
- React 19, TypeScript, Vite, Vitest, lucide-react
- Docker Compose, Kubernetes manifests, GitHub Actions

## Run the API Locally

```bash
uv sync --all-groups
uv run uvicorn modelledger.api.app:app --reload --port 8088
```

Open `http://127.0.0.1:8088/docs`.

Demo users:

- `admin`
- `approver`
- `scientist`
- `viewer`

All demo users use password `modelledger-demo`.

## Run the Console

```bash
cd web
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

## Run the Full Stack

```bash
docker compose up --build
```

Ports:

- API: `http://127.0.0.1:8088`
- React console: `http://127.0.0.1:5178`
- PostgreSQL: `127.0.0.1:5547`
- Redis: `127.0.0.1:6387`
- MinIO API: `http://127.0.0.1:9007`
- MinIO console: `http://127.0.0.1:9008`

## Verification

```bash
uv run ruff check .
uv run pytest --cov=modelledger
cd web
npm run test
npm run build
```

Set `MODELLEDGER_TEST_DATABASE_URL` to enable PostgreSQL-backed integration tests:

```bash
MODELLEDGER_TEST_DATABASE_URL=postgresql+psycopg://modelledger:modelledger@localhost:5547/modelledger uv run pytest
```

## Project Structure

```text
modelledger/
  api/                  FastAPI routes and dependency guards
  integrations/         Optional MLflow and MinIO adapters
  services/             Domain workflows
  db.py                 Engine/session setup
  models.py             SQLAlchemy models
  policies.py           Risk-tiered evaluation policies
  security.py           Demo auth and JWT helpers
  tasks.py              Celery task entry points
tests/                  Backend unit, API, and integration tests
web/                    React + TypeScript console
deploy/kubernetes/      API and worker manifests
docs/                   Architecture, API, governance, and operations notes
```

## Production Notes

This repository demonstrates governance control-plane behavior. It does not
serve models or execute untrusted model artifacts. Production deployments should
replace demo authentication, enforce TLS, configure object storage credentials
through secrets, run Alembic migrations explicitly, isolate Celery queues by
workload, and define retention policies for audit and artifact metadata.
