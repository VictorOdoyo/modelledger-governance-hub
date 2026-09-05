from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from modelledger.enums import Role
from modelledger.settings import Settings, get_settings

password_hash = PasswordHash.recommended()


class AuthError(ValueError):
    pass


DEMO_USERS: dict[str, tuple[str, Role]] = {
    "admin": ("modelledger-demo", Role.ADMIN),
    "approver": ("modelledger-demo", Role.APPROVER),
    "scientist": ("modelledger-demo", Role.SCIENTIST),
    "viewer": ("modelledger-demo", Role.VIEWER),
}


def verify_demo_user(username: str, password: str) -> Role | None:
    record = DEMO_USERS.get(username)
    if record is None:
        return None
    expected, role = record
    return role if password == expected else None


def create_access_token(username: str, role: Role, settings: Settings | None = None) -> str:
    cfg = settings or get_settings()
    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": username,
        "role": role.value,
        "iss": cfg.jwt_issuer,
        "aud": cfg.jwt_audience,
        "iat": now,
        "exp": now + timedelta(minutes=cfg.access_token_minutes),
    }
    return jwt.encode(payload, cfg.jwt_secret, algorithm="HS256")


def decode_access_token(token: str, settings: Settings | None = None) -> tuple[str, Role]:
    cfg = settings or get_settings()
    try:
        payload = jwt.decode(
            token,
            cfg.jwt_secret,
            algorithms=["HS256"],
            issuer=cfg.jwt_issuer,
            audience=cfg.jwt_audience,
        )
    except jwt.PyJWTError as exc:
        raise AuthError("invalid token") from exc
    username = str(payload.get("sub", ""))
    try:
        role = Role(str(payload.get("role", "")))
    except ValueError as exc:
        raise AuthError("invalid role") from exc
    if not username:
        raise AuthError("invalid subject")
    return username, role
