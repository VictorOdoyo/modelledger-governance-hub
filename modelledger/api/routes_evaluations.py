from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from modelledger.api.dependencies import CurrentUser, current_user, get_session
from modelledger.schemas import EvaluationRead, EvaluationRequest, GateDecision
from modelledger.services.evaluations import evaluate_version, list_gate_results
from modelledger.services.registry import get_model, get_version

router = APIRouter(prefix="/versions/{version_id}/evaluations", tags=["evaluations"])


@router.post("", response_model=EvaluationRead)
def run_evaluation(
    version_id: str,
    payload: EvaluationRequest,
    session: Session = Depends(get_session),
    user: CurrentUser = Depends(current_user),
):
    version = get_version(session, version_id)
    if version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="version not found")
    model = get_model(session, version.model_id)
    assert model is not None
    results = evaluate_version(session, model, version, payload, user.username)
    session.commit()
    return EvaluationRead(
        version_id=version.id,
        state=version.gate_state,
        decisions=[
            GateDecision(
                name=result.name,
                state=result.state,
                observed=result.observed,
                threshold=result.threshold,
                message=result.message,
            )
            for result in results
        ],
    )


@router.get("", response_model=EvaluationRead)
def read_evaluation(version_id: str, session: Session = Depends(get_session)):
    version = get_version(session, version_id)
    if version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="version not found")
    results = list_gate_results(session, version_id)
    return EvaluationRead(
        version_id=version.id,
        state=version.gate_state,
        decisions=[
            GateDecision(
                name=result.name,
                state=result.state,
                observed=result.observed,
                threshold=result.threshold,
                message=result.message,
            )
            for result in results
        ],
    )
