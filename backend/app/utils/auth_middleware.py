"""
ObMind Auth Middleware
Flask decorator to protect routes with JWT authentication.

Usage:
    from app.utils.auth_middleware import require_auth, require_verified

    @app.route('/api/protected')
    @require_auth
    def protected_route():
        user_id = g.user_id
        ...

    @app.route('/api/verified-only')
    @require_verified
    def verified_only():
        user_id = g.user_id
        ...
"""

import logging
from functools import wraps

from flask import request, jsonify, g

from .jwt_utils import decode_token, TokenExpiredError, TokenInvalidError

logger = logging.getLogger("obmind.auth_middleware")


def _extract_bearer_token() -> str | None:
    """Extract the raw JWT from the Authorization: Bearer <token> header."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[len("Bearer "):]
    return None


def get_current_user_id() -> str | None:
    """Helper to extract user_id if valid bearer token is present, else None."""
    token = _extract_bearer_token()
    if not token:
        return None
    try:
        payload = decode_token(token, expected_type="access")
        return payload.get("sub")
    except Exception:
        return None


def optional_auth(f):
    """
    Decorator: If valid JWT access token is present, sets g.user_id and g.is_verified.
    If no token or invalid, still executes route with g.user_id = None.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        g.user_id = get_current_user_id()
        g.is_verified = False
        return f(*args, **kwargs)
    return decorated


def require_auth(f):
    """
    Decorator: Requires a valid (not necessarily verified) JWT access token.
    Sets g.user_id and g.is_verified on success.
    Returns 401 on missing/invalid/expired token.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = _extract_bearer_token()
        if not token:
            return jsonify({
                "success": False,
                "error": "Authentication required. Please log in.",
                "code": "MISSING_TOKEN"
            }), 401

        try:
            payload = decode_token(token, expected_type="access")
        except TokenExpiredError:
            return jsonify({
                "success": False,
                "error": "Session expired. Please log in again.",
                "code": "TOKEN_EXPIRED"
            }), 401
        except TokenInvalidError as exc:
            logger.warning(f"Invalid token attempt: {exc}")
            return jsonify({
                "success": False,
                "error": "Invalid authentication token.",
                "code": "TOKEN_INVALID"
            }), 401

        g.user_id = payload["sub"]
        g.is_verified = payload.get("is_verified", False)
        return f(*args, **kwargs)

    return decorated


def require_verified(f):
    """
    Decorator: Like require_auth but also requires email verification.
    Returns 403 if logged in but email not yet verified.
    """
    @wraps(f)
    @require_auth
    def decorated(*args, **kwargs):
        if not g.is_verified:
            return jsonify({
                "success": False,
                "error": "Please verify your email address before accessing this feature.",
                "code": "EMAIL_NOT_VERIFIED"
            }), 403
        return f(*args, **kwargs)

    return decorated
