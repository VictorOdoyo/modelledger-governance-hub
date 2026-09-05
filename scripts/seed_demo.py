from sqlalchemy.orm import Session

from modelledger.db import SessionLocal, create_schema
from modelledger.enums import GateState, RiskTier
from modelledger.schemas import ApprovalRequestCreate, ModelCreate, VersionCreate
from modelledger.services.approvals import decide_approval, request_approval
from modelledger.services.registry import create_model, create_version


def seed(session: Session) -> None:
    model = create_model(
        session,
        ModelCreate(
            name="Claims Triage",
            owner="risk-platform",
            business_domain="insurance",
            risk_tier=RiskTier.HIGH,
            tags=["claims", "regulated"],
        ),
        actor="admin",
    )
    version = create_version(
        session,
        model,
        VersionCreate(
            semantic_version="1.4.0",
            source_run_id="run-demo-claims",
            artifact_uri="s3://model-artifacts/claims/1.4.0/model.pkl",
            training_dataset="claims-2026-q3",
            metrics={"auc": 0.91, "latency_ms": 230, "data_quality": 0.99, "bias_gap": 0.04},
            feature_signature=["claim_type", "region", "prior_claim_count"],
        ),
        actor="admin",
    )
    version.gate_state = GateState.PASSED
    approval = request_approval(
        session,
        version,
        ApprovalRequestCreate(reason="Demo production package approved for local walkthrough."),
        actor="scientist",
    )
    decide_approval(session, approval, actor="approver", approved=True, note="Demo approval")


if __name__ == "__main__":
    create_schema()
    with SessionLocal() as session:
        seed(session)
        session.commit()
    print("Seeded demo governance data.")
