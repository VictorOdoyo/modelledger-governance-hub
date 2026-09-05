from fastapi import APIRouter, HTTPException, status

from modelledger.schemas import TokenRequest, TokenResponse
from modelledger.security import create_access_token, verify_demo_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def issue_token(payload: TokenRequest) -> TokenResponse:
    role = verify_demo_user(payload.username, payload.password)
    if role is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    return TokenResponse(access_token=create_access_token(payload.username, role), role=role)
