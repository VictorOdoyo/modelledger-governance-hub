import os

import pytest
from sqlalchemy.orm import sessionmaker

from modelledger.db import Base, make_engine
from modelledger.enums import DeploymentStage, GateState, RiskTier
from modelledger.schemas import (
    ApprovalRequestCreate,
    DeploymentRequest,
    EvaluationRequest,
    ModelCreate,
    VersionCreate,
)
from modelledger.services.approvals import decide_approval, request_approval
from modelledger.services.deployments import create_deployment
from modelledger.services.evaluations import evaluate_version
from modelledger.services.registry import create_model, create_version


@pytest.mark.skipif(
    not os.getenv("MODELLEDGER_TEST_DATABASE_URL"),
    reason="set MODELLEDGER_TEST_DATABASE_URL for PostgreSQL integration coverage",
)
def test_governed_release_flow_commits_against_postgres():
    engine = make_engine(os.environ["MODELLEDGER_TEST_DATABASE_URL"])
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as session:
        model = create_model(
            session,
            ModelCreate(name="Claims QA", owner="risk", business_domain="insurance", risk_tier=RiskTier.HIGH),
            "scientist",
        )
        version = create_version(
            session,
            model,
            VersionCreate(
                semantic_version="1.0.0",
                source_run_id="run-pg-1",
                artifact_uri="s3://model-artifacts/claimsqa/1.0.0/model.pkl",
                training_dataset="claims-postgres",
            ),
            "scientist",
        )
        evaluate_version(
            session,
            model,
            version,
            EvaluationRequest(metrics={"auc": 0.91, "latency_ms": 200, "data_quality": 0.99, "bias_gap": 0.03}),
            "scientist",
        )
        approval = request_approval(
            session,
            version,
            ApprovalRequestCreate(reason="PostgreSQL-backed release package is ready."),
            "scientist",
        )
        decide_approval(session, approval, "approver", True, "Approved through integration test")
        deployment = create_deployment(
            session,
            version,
            DeploymentRequest(target_stage=DeploymentStage.PRODUCTION, change_ticket="CHG-PG", environment="prod"),
            "scientist",
        )
        session.commit()
        assert version.gate_state == GateState.PASSED
        assert deployment.stage == DeploymentStage.PRODUCTION
