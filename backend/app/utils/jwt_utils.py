"""
ObMind JWT Utilities
Handles creation and validation of access + refresh tokens.

Token design:
  - Access token:  short-lived (15 min), carries user_id + is_verified
  - Refresh token: long-lived (30 days), single-use rotation recommended
  - All tokens are HS256 signed using SECRET_KEY from config

Usage:
  token = create_access_token(user_id="...", is_verified=True)
  payload = decode_token(token)   # raises on invalid/expired
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

_SECRET = os.environ.get("SECRET_KEY", "obmind-secret-key-change-in-production")
_ALGORITHM = "HS256"

_ACCESS_TTL_MINUTES = int(os.environ.get("JWT_ACCESS_TTL_MINUTES", "15"))
_REFRESH_TTL_DAYS = int(os.environ.get("JWT_REFRESH_TTL_DAYS", "30"))


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ------------------------------------------------------------------ #
# Token creation
# ------------------------------------------------------------------ #

def create_access_token(user_id: str, is_verified: bool) -> str:
    """
    Issue a short-lived access token.
    Payload: sub, is_verified, type='access', exp, iat
    """
    now = _utcnow()
    payload = {
        "sub": user_id,
        "is_verified": is_verified,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=_ACCESS_TTL_MINUTES),
    }
    return jwt.encode(payload, _SECRET, algorithm=_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """
    Issue a long-lived refresh token.
    Payload: sub, type='refresh', exp, iat
    """
    now = _utcnow()
    payload = {
        "sub": user_id,
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=_REFRESH_TTL_DAYS),
    }
    return jwt.encode(payload, _SECRET, algorithm=_ALGORITHM)


# ------------------------------------------------------------------ #
# Token validation
# ------------------------------------------------------------------ #

class TokenError(Exception):
    """Base class for all token errors — map to 401 HTTP responses."""
    pass

class TokenExpiredError(TokenError):
    pass

class TokenInvalidError(TokenError):
    pass


def decode_token(token: str, expected_type: Optional[str] = None) -> dict:
    """
    Decode and validate a JWT.

    Args:
        token:         Raw JWT string from Authorization header.
        expected_type: If provided ('access' or 'refresh'), validates
                       the 'type' claim to prevent token misuse.

    Returns:
        Decoded payload dict.

    Raises:
        TokenExpiredError: Token has expired.
        TokenInvalidError: Any other validation failure (bad sig, malformed, wrong type).
    """
    try:
        payload = jwt.decode(token, _SECRET, algorithms=[_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token has expired. Please log in again.")
    except jwt.InvalidTokenError as exc:
        raise TokenInvalidError(f"Invalid token: {exc}")

    if expected_type and payload.get("type") != expected_type:
        raise TokenInvalidError(
            f"Expected token type '{expected_type}', got '{payload.get('type')}'."
        )

    return payload
