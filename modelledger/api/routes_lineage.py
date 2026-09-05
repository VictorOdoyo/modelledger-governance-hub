from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from modelledger.api.dependencies import get_session
from modelledger.services.lineage import build_lineage_graph
from modelledger.services.registry import get_model, get_version

router = APIRouter(prefix="/versions/{version_id}/lineage", tags=["lineage"])


@router.get("")
def read_lineage(version_id: str, session: Session = Depends(get_session)):
    version = get_version(session, version_id)
    if version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="version not found")
    model = get_model(session, version.model_id)
    assert model is not None
    return build_lineage_graph(model.name, version.training_dataset, version.source_run_id, version.id)
