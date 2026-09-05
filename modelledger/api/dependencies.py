from collections.abc import Callable
from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status

from modelledger.db import get_session
from modelledger.enums import Role
from modelledger.security import AuthError, decode_access_token


@dataclass(frozen=True)
class CurrentUser:
    username: str
    role: Role


def current_user(authorization: str | None = Header(default=None)) -> CurrentUser:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing bearer token")
    try:
        username, role = decode_access_token(authorization.split(" ", 1)[1])
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token") from exc
    return CurrentUser(username=username, role=role)


def require_role(*roles: Role) -> Callable[[CurrentUser], CurrentUser]:
    def guard(user: CurrentUser = Depends(current_user)) -> CurrentUser:
        if user.role not in roles and user.role != Role.ADMIN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="insufficient role")
        return user

    return guard


DbSession = Depends(get_session)
