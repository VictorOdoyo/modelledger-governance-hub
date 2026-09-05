from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

from modelledger.api import (
    routes_approvals,
    routes_artifacts,
    routes_audit,
    routes_auth,
    routes_deployments,
    routes_drift,
    routes_evaluations,
    routes_lineage,
    routes_models,
    routes_summary,
)
from modelledger.db import create_schema
from modelledger.settings import get_settings

REQUESTS = Counter("modelledger_http_requests_total", "Total HTTP requests", ["path"])


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        create_schema()
        yield

    app = FastAPI(
        title="ModelLedger Governance Hub",
        version="0.1.0",
        summary="Model registry, evaluation gates, approvals, deployment stages, and drift reports.",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def count_requests(request, call_next):
        REQUESTS.labels(path=request.url.path).inc()
        return await call_next(request)

    @app.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "live"}

    @app.get("/health/ready")
    def ready() -> dict[str, str]:
        return {"status": "ready"}

    @app.get("/metrics")
    def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    prefix = "/api/v1"
    app.include_router(routes_auth.router, prefix=prefix)
    app.include_router(routes_models.router, prefix=prefix)
    app.include_router(routes_evaluations.router, prefix=prefix)
    app.include_router(routes_approvals.router, prefix=prefix)
    app.include_router(routes_deployments.router, prefix=prefix)
    app.include_router(routes_drift.router, prefix=prefix)
    app.include_router(routes_artifacts.router, prefix=prefix)
    app.include_router(routes_audit.router, prefix=prefix)
    app.include_router(routes_summary.router, prefix=prefix)
    app.include_router(routes_lineage.router, prefix=prefix)
    return app


app = create_app()
