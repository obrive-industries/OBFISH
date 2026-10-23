"""
Brain Auth Middleware
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

logger = logging.getLogger("brain.auth_middleware")


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


def get_current_user():
    """Return the User model instance for the current authenticated request, or None."""
    uid = get_current_user_id()
    if not uid:
        return None
    try:
        from ..models.user import User, db
        return db.session.get(User, uid)
    except Exception as e:
        logger.warning(f"Failed to fetch user {uid}: {e}")
        return None


def get_user_llm_client(user=None):
    """
    Return an LLMClient initialized with the user's BYOK credentials if provided,
    otherwise falling back to platform defaults from Config.
    """
    from .llm_client import LLMClient
    from ..config import Config

    target_user = user or get_current_user()
    if target_user and isinstance(getattr(target_user, "custom_llm_api_key", None), str) and target_user.custom_llm_api_key:
        raw_base = getattr(target_user, "custom_llm_base_url", None)
        base_url = raw_base if isinstance(raw_base, str) and raw_base else Config.LLM_BASE_URL
        raw_model = getattr(target_user, "custom_llm_model_name", None)
        model_name = raw_model if isinstance(raw_model, str) and raw_model else None
        from .llm_client import resolve_default_model
        resolved_model = resolve_default_model(base_url, model_name)
        logger.info(f"Using BYOK credentials for user: {getattr(target_user, 'email', '')} (model={resolved_model})")
        return LLMClient(
            api_key=target_user.custom_llm_api_key,
            base_url=base_url,
            model=resolved_model
        )
    return LLMClient()


def check_simulation_permission(user=None) -> tuple[bool, str | None]:
    """
    Enforces email verification and BYOK (Bring Your Own Key) LLM credentials for simulation/ontology workflows.
    Returns (True, None) if permitted, or (False, error_msg) if blocked.
    """
    target_user = user or get_current_user()
    if not target_user:
        return False, "Authentication required. Please sign in to run simulations."
    if not target_user.is_verified:
        return False, "Please verify your email address before running simulations."
    require_byok = True
    try:
        from flask import current_app
        if current_app:
            require_byok = current_app.config.get("REQUIRE_BYOK", True)
    except Exception:
        from ..config import Config
        require_byok = getattr(Config, 'REQUIRE_BYOK', True)

    if require_byok and not target_user.custom_llm_api_key:
        return False, "LLM API Key required. Please configure your custom API key (BYOK) in your profile settings before starting a simulation."
    return True, None

