from tests.conftest import auth_header


def test_auth_endpoint_issues_demo_token(client):
    response = client.post(
        "/api/v1/auth/token",
        json={"username": "scientist", "password": "modelledger-demo"},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "scientist"


def test_model_version_evaluation_approval_and_deployment_flow(client, scientist_token, approver_token):
    model_response = client.post(
        "/api/v1/models",
        headers=auth_header(scientist_token),
        json={
            "name": "Revenue Forecast",
            "owner": "finance-ml",
            "business_domain": "finance",
            "risk_tier": "medium",
            "tags": ["forecasting"],
        },
    )
    assert model_response.status_code == 201
    model_id = model_response.json()["id"]

    version_response = client.post(
        f"/api/v1/models/{model_id}/versions",
        headers=auth_header(scientist_token),
        json={
            "semantic_version": "2.1.0",
            "source_run_id": "run-222",
            "artifact_uri": "s3://model-artifacts/revenue/2.1.0/model.pkl",
            "training_dataset": "revenue-q3",
            "metrics": {},
            "feature_signature": ["region", "segment"],
        },
    )
    assert version_response.status_code == 201
    version_id = version_response.json()["id"]

    eval_response = client.post(
        f"/api/v1/versions/{version_id}/evaluations",
        headers=auth_header(scientist_token),
        json={"metrics": {"auc": 0.88, "latency_ms": 410, "data_quality": 0.98, "bias_gap": 0.04}},
    )
    assert eval_response.status_code == 200
    assert eval_response.json()["state"] == "passed"

    approval_response = client.post(
        f"/api/v1/approvals/versions/{version_id}",
        headers=auth_header(scientist_token),
        json={"reason": "Production controls and metrics are ready for review."},
    )
    assert approval_response.status_code == 201
    approval_id = approval_response.json()["id"]

    decision_response = client.post(
        f"/api/v1/approvals/{approval_id}/approve",
        headers=auth_header(approver_token),
        json={"note": "Approved for limited production"},
    )
    assert decision_response.status_code == 200

    deployment_response = client.post(
        f"/api/v1/deployments/versions/{version_id}",
        headers=auth_header(scientist_token),
        json={"target_stage": "production", "change_ticket": "CHG-2026", "environment": "prod-us"},
    )
    assert deployment_response.status_code == 201
    assert deployment_response.json()["stage"] == "production"


def test_viewer_cannot_register_model(client):
    token = client.post(
        "/api/v1/auth/token",
        json={"username": "viewer", "password": "modelledger-demo"},
    ).json()["access_token"]
    response = client.post(
        "/api/v1/models",
        headers=auth_header(token),
        json={
            "name": "Blocked",
            "owner": "viewer",
            "business_domain": "demo",
            "risk_tier": "low",
            "tags": [],
        },
    )
    assert response.status_code == 403
