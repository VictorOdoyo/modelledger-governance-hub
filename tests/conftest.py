import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from modelledger.api.app import create_app
from modelledger.db import Base, get_session, make_engine
from modelledger.enums import RiskTier, Role
from modelledger.schemas import ModelCreate, VersionCreate
from modelledger.security import create_access_token
from modelledger.services.registry import create_model, create_version


@pytest.fixture
def session():
    engine = make_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as session:
        yield session


@pytest.fixture
def seeded(session):
    model = create_model(
        session,
        ModelCreate(
            name="Claims Triage",
            owner="risk-platform",
            business_domain="insurance",
            risk_tier=RiskTier.HIGH,
            tags=["claims", "triage"],
        ),
        actor="scientist",
    )
    version = create_version(
        session,
        model,
        VersionCreate(
            semantic_version="1.4.0",
            source_run_id="run-2026-09-claims",
            artifact_uri="s3://model-artifacts/claims/1.4.0/model.pkl",
            training_dataset="claims-2026-q3",
            metrics={"auc": 0.91, "latency_ms": 210, "data_quality": 0.99, "bias_gap": 0.04},
            feature_signature=["age_band", "claim_type", "region"],
        ),
        actor="scientist",
    )
    session.commit()
    return model, version


@pytest.fixture
def client():
    engine = make_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)

    def override_session():
        with factory() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = override_session
    return TestClient(app)


@pytest.fixture
def scientist_token():
    return create_access_token("scientist", role=Role.SCIENTIST)


@pytest.fixture
def approver_token():
    return create_access_token("approver", role=Role.APPROVER)


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
