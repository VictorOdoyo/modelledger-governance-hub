from modelledger.schemas import ArtifactCreate
from modelledger.services.artifacts import calculate_sha256, list_artifacts, register_artifact


def test_artifact_registration_records_digest(session, seeded):
    _, version = seeded
    digest = calculate_sha256(b"model bytes")
    artifact = register_artifact(
        session,
        version,
        ArtifactCreate(
            uri="s3://model-artifacts/claims/1.4.0/model.pkl",
            sha256=digest,
            content_type="application/octet-stream",
            size_bytes=11,
        ),
        actor="scientist",
    )
    session.commit()

    assert artifact.sha256 == digest
    assert list_artifacts(session, version.id)[0].id == artifact.id
