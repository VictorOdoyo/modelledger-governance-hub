# Operations

Run the API locally with SQLite for development:

```bash
uv run uvicorn modelledger.api.app:app --reload --port 8088
```

Run the full backing stack:

```bash
docker compose up --build
```

Demo users are `admin`, `approver`, `scientist`, and `viewer`; the local password
is `modelledger-demo`.

For production, set a unique `MODELLEDGER_JWT_SECRET`, enforce TLS at the ingress,
configure PostgreSQL backups, restrict MinIO credentials, and separate worker
queues for evaluation, drift, and report generation.
