import pytest

from modelledger.enums import Role
from modelledger.security import (
    AuthError,
    create_access_token,
    decode_access_token,
    verify_demo_user,
)


def test_demo_user_maps_to_role():
    assert verify_demo_user("approver", "modelledger-demo") == Role.APPROVER
    assert verify_demo_user("approver", "wrong-password") is None


def test_access_token_round_trip_preserves_role():
    token = create_access_token("scientist", Role.SCIENTIST)
    assert decode_access_token(token) == ("scientist", Role.SCIENTIST)


def test_invalid_token_is_rejected():
    with pytest.raises(AuthError):
        decode_access_token("not-a-token")
