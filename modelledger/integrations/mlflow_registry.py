from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MlflowVersionLink:
    name: str
    version: str
    run_id: str
    artifact_uri: str


class MlflowRegistry:
    def __init__(self, tracking_uri: str) -> None:
        self.tracking_uri = tracking_uri

    def create_registered_version(self, link: MlflowVersionLink) -> dict[str, Any]:
        import mlflow

        mlflow.set_tracking_uri(self.tracking_uri)
        client = mlflow.tracking.MlflowClient()
        registered = client.create_model_version(
            name=link.name, source=link.artifact_uri, run_id=link.run_id
        )
        return {"name": registered.name, "version": registered.version, "run_id": link.run_id}
