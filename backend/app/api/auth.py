"""
ObMind Auth API — /api/auth/*
All authentication endpoints:

  POST /api/auth/register         Sign up with email + password
  POST /api/auth/login            Log in, receive access + refresh tokens
  POST /api/auth/refresh          Exchange refresh token for new access token
  POST /api/auth/logout           Invalidate refresh token (client-side for stateless)
  GET  /api/auth/verify-email     Verify email address using token from link
  POST /api/auth/resend-verification  Re-send verification email
  POST /api/auth/forgot-password  Request password reset email
  POST /api/auth/reset-password   Set new password with reset token
  GET  /api/auth/me               Get current user profile (requires auth)

Security posture:
  - Passwords: bcrypt (cost 12) — never stored in plaintext
  - Tokens: HS256 JWT, access=15 min, refresh=30 days
  - Email verification: 64-byte URL-safe token, 24h expiry
  - Password reset: 64-byte token, 30-minute expiry
  - All validation errors return consistent shape: {success, error, code}
  - Rate limiting: apply via nginx/Cloudflare in production
"""

import re
import logging
from datetime import datetime, timezone

from flask import Blueprint, request, jsonify, g

from ..models.user import User, db
from ..utils.jwt_utils import (
    create_access_token, create_refresh_token,
    decode_token, TokenExpiredError, TokenInvalidError
)
from ..utils.auth_middleware import require_auth
from ..services.email_service import (
    send_verification_email,
    send_password_reset_email,
    send_welcome_email,
)

logger = logging.getLogger("obmind.api.auth")

auth_bp = Blueprint("auth", __name__)


# ------------------------------------------------------------------ #
# Validators
# ------------------------------------------------------------------ #

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
_MIN_PASSWORD_LEN = 8
_MAX_PASSWORD_LEN = 128


def _validate_email(email: str) -> str | None:
    """Return error string or None."""
    if not email or not isinstance(email, str):
        return "Email address is required."
    email = email.strip().lower()
    if not _EMAIL_RE.match(email):
        return "Please enter a valid email address."
    return None


def _validate_password(password: str) -> str | None:
    """Return error string or None."""
    if not password or not isinstance(password, str):
        return "Password is required."
    if len(password) < _MIN_PASSWORD_LEN:
        return f"Password must be at least {_MIN_PASSWORD_LEN} characters."
    if len(password) > _MAX_PASSWORD_LEN:
        return f"Password must not exceed {_MAX_PASSWORD_LEN} characters."
    return None


def _validate_full_name(name: str) -> str | None:
    if not name or not isinstance(name, str) or not name.strip():
        return "Full name is required."
    if len(name.strip()) < 2:
        return "Full name must be at least 2 characters."
    if len(name.strip()) > 100:
        return "Full name must not exceed 100 characters."
    return None


def _err(message: str, code: str = "VALIDATION_ERROR", status: int = 400):
    return jsonify({"success": False, "error": message, "code": code}), status


def _ok(data: dict, status: int = 200):
    return jsonify({"success": True, **data}), status


# ------------------------------------------------------------------ #
# POST /api/auth/register
# ------------------------------------------------------------------ #

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user account.

    Body: { email, password, full_name }

    Flow:
      1. Validate inputs
      2. Check email uniqueness
      3. Create User, hash password, generate verification token
      4. Commit to DB
      5. Send verification email (async-safe: logged if SMTP not configured)
      6. Return access + refresh tokens (user can use the app immediately,
         but simulation features require verification)
    """
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    full_name = (data.get("full_name") or "").strip()

    # Validate
    if err := _validate_email(email):
        return _err(err)
    if err := _validate_password(password):
        return _err(err)
    if err := _validate_full_name(full_name):
        return _err(err)

    # Check uniqueness
    if User.query.filter_by(email=email).first():
        return _err(
            "An account with this email already exists. Please log in or use a different email.",
            code="EMAIL_TAKEN"
        )

    # Create user
    user = User(email=email, full_name=full_name)
    user.set_password(password)
    token = user.generate_verification_token(ttl_hours=24)

    db.session.add(user)
    db.session.commit()

    logger.info(f"New user registered: {email} (id={user.id})")

    # Send verification email (non-blocking — failure doesn't fail registration)
    email_sent = send_verification_email(user.email, user.full_name, token)
    if not email_sent:
        logger.warning(f"Verification email failed to send for {email}")

    # Issue tokens immediately — user can explore, but sim features need verification
    access = create_access_token(user.id, is_verified=False)
    refresh = create_refresh_token(user.id)

    return _ok({
        "message": (
            "Account created! Please check your email to verify your account. "
            "You can start exploring ObMind, but simulation runs require verification."
        ),
        "access_token": access,
        "refresh_token": refresh,
        "user": user.to_public_dict(),
        "email_sent": email_sent,
    }, status=201)


# ------------------------------------------------------------------ #
# POST /api/auth/login
# ------------------------------------------------------------------ #

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate with email + password.

    Body: { email, password }

    Returns: access_token, refresh_token, user profile.
    Note: unverified users CAN log in — they just can't run simulations.
    """
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return _err("Email and password are required.")

    user = User.query.filter_by(email=email).first()

    # Use constant-time comparison — always call check_password to prevent timing attacks
    if not user or not user.check_password(password):
        return _err(
            "Invalid email or password.",
            code="INVALID_CREDENTIALS",
            status=401
        )

    if not user.is_active:
        return _err(
            "Your account has been deactivated. Please contact support.",
            code="ACCOUNT_DEACTIVATED",
            status=403
        )

    # Update last login
    user.last_login_at = datetime.now(timezone.utc)
    db.session.commit()

    logger.info(f"User logged in: {email} (verified={user.is_verified})")

    access = create_access_token(user.id, is_verified=user.is_verified)
    refresh = create_refresh_token(user.id)

    return _ok({
        "access_token": access,
        "refresh_token": refresh,
        "user": user.to_public_dict(),
    })


# ------------------------------------------------------------------ #
# POST /api/auth/refresh
# ------------------------------------------------------------------ #

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    """
    Exchange a valid refresh token for a new access token.

    Body: { refresh_token }

    The frontend should call this transparently when a 401 TOKEN_EXPIRED
    is returned on an API call.
    """
    data = request.get_json(silent=True) or {}
    raw_refresh = data.get("refresh_token") or ""

    if not raw_refresh:
        return _err("Refresh token is required.", code="MISSING_TOKEN", status=401)

    try:
        payload = decode_token(raw_refresh, expected_type="refresh")
    except TokenExpiredError:
        return _err("Session expired. Please log in again.", code="TOKEN_EXPIRED", status=401)
    except TokenInvalidError:
        return _err("Invalid refresh token.", code="TOKEN_INVALID", status=401)

    user = db.session.get(User, payload["sub"])
    if not user or not user.is_active:
        return _err("User not found or deactivated.", code="USER_NOT_FOUND", status=401)

    new_access = create_access_token(user.id, is_verified=user.is_verified)
    return _ok({
        "access_token": new_access,
        "user": user.to_public_dict(),
    })


# ------------------------------------------------------------------ #
# GET /api/auth/verify-email?token=<token>
# ------------------------------------------------------------------ #

@auth_bp.route("/verify-email", methods=["GET", "POST"])
def verify_email():
    """
    Verify a user's email address using the token from the verification link.

    Query param or JSON body: token

    On success: marks user as verified, sends welcome email, returns
    fresh access token with is_verified=True so the frontend can update state.
    """
    token = (request.args.get("token") or (request.get_json(silent=True) or {}).get("token") or "").strip()
    if not token:
        return _err("Verification token is missing.", code="MISSING_TOKEN")

    # Find user by token
    user = User.query.filter_by(verification_token=token).first()

    if not user:
        return _err(
            "This verification link is invalid or has already been used.",
            code="TOKEN_INVALID"
        )

    if user.is_verified:
        return _ok({"message": "Your email is already verified. You're all set!"})

    if user.is_verification_token_expired():
        return _err(
            "This verification link has expired. Please request a new one.",
            code="TOKEN_EXPIRED"
        )

    # Verify
    if not user.verify_email(token):
        return _err("Email verification failed. Please try again.", code="VERIFICATION_FAILED")

    db.session.commit()
    logger.info(f"Email verified: {user.email}")

    # Send welcome email
    send_welcome_email(user.email, user.full_name)

    # Return updated access token so frontend can reflect verified state immediately
    new_access = create_access_token(user.id, is_verified=True)

    return _ok({
        "message": "Email verified successfully! Welcome to ObMind.",
        "access_token": new_access,
        "user": user.to_public_dict(),
    })


# ------------------------------------------------------------------ #
# POST /api/auth/resend-verification
# ------------------------------------------------------------------ #

@auth_bp.route("/resend-verification", methods=["POST"])
def resend_verification():
    """
    Re-send the verification email (e.g. if the first one expired or was lost).

    Body: { email }
    """
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()

    if not email:
        return _err("Email address is required.")

    user = User.query.filter_by(email=email).first()

    # Always return the same response to prevent user enumeration
    generic_ok = _ok({
        "message": "If an unverified account exists with that email, a new verification link has been sent."
    })

    if not user or user.is_verified:
        return generic_ok

    token = user.generate_verification_token(ttl_hours=24)
    db.session.commit()
    send_verification_email(user.email, user.full_name, token)

    return generic_ok


# ------------------------------------------------------------------ #
# POST /api/auth/forgot-password
# ------------------------------------------------------------------ #

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    """
    Request a password reset email.

    Body: { email }

    Always returns the same message regardless of whether the email exists
    — this prevents email enumeration attacks.
    """
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()

    generic_ok = _ok({
        "message": "If an account with that email exists, a password reset link has been sent. Check your inbox."
    })

    if not email:
        return generic_ok

    user = User.query.filter_by(email=email).first()
    if not user or not user.is_active:
        return generic_ok

    token = user.generate_reset_token(ttl_minutes=30)
    db.session.commit()
    send_password_reset_email(user.email, user.full_name, token)

    logger.info(f"Password reset requested for: {email}")
    return generic_ok


# ------------------------------------------------------------------ #
# POST /api/auth/reset-password
# ------------------------------------------------------------------ #

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """
    Set a new password using a valid reset token.

    Body: { token, new_password }
    """
    data = request.get_json(silent=True) or {}
    token = (data.get("token") or "").strip()
    new_password = data.get("new_password") or ""

    if not token:
        return _err("Reset token is required.", code="MISSING_TOKEN")

    if err := _validate_password(new_password):
        return _err(err)

    user = User.query.filter_by(reset_token=token).first()

    if not user:
        return _err(
            "This reset link is invalid or has already been used.",
            code="TOKEN_INVALID"
        )

    if not user.reset_password(token, new_password):
        return _err(
            "This reset link has expired. Please request a new one.",
            code="TOKEN_EXPIRED"
        )

    db.session.commit()
    logger.info(f"Password reset successful for: {user.email}")

    return _ok({"message": "Password updated successfully. You can now log in with your new password."})


# ------------------------------------------------------------------ #
# GET /api/auth/me
# ------------------------------------------------------------------ #

@auth_bp.route("/me", methods=["GET"])
@require_auth
def me():
    """
    Return the current user's public profile.
    Requires: valid access token.
    """
    user = db.session.get(User, g.user_id)
    if not user:
        return _err("User not found.", code="USER_NOT_FOUND", status=404)

    return _ok({"user": user.to_public_dict()})


# ------------------------------------------------------------------ #
# PUT /api/auth/profile (Update name & BYOK settings)
# ------------------------------------------------------------------ #

@auth_bp.route("/profile", methods=["PUT", "PATCH"])
@require_auth
def update_profile():
    """
    Update profile fields, including BYOK (Bring Your Own Key) LLM settings.
    Body: { full_name?, custom_llm_api_key?, custom_llm_base_url?, custom_llm_model_name? }
    """
    user = db.session.get(User, g.user_id)
    if not user:
        return _err("User not found.", code="USER_NOT_FOUND", status=404)

    data = request.get_json(silent=True) or {}

    if "full_name" in data:
        name = (data["full_name"] or "").strip()
        if err := _validate_full_name(name):
            return _err(err)
        user.full_name = name

    # BYOK settings
    if "custom_llm_api_key" in data:
        key = data["custom_llm_api_key"]
        user.custom_llm_api_key = key.strip() if key else None

    if "custom_llm_base_url" in data:
        base_url = data["custom_llm_base_url"]
        user.custom_llm_base_url = base_url.strip() if base_url else None

    if "custom_llm_model_name" in data:
        model = data["custom_llm_model_name"]
        user.custom_llm_model_name = model.strip() if model else None

    db.session.commit()
    logger.info(f"User profile updated: {user.email}")

    return _ok({
        "message": "Profile updated successfully.",
        "user": user.to_public_dict()
    })


# ------------------------------------------------------------------ #
# POST /api/auth/change-password
# ------------------------------------------------------------------ #

@auth_bp.route("/change-password", methods=["POST"])
@require_auth
def change_password():
    """
    Change password for currently authenticated user.
    Body: { current_password, new_password }
    """
    user = db.session.get(User, g.user_id)
    if not user:
        return _err("User not found.", code="USER_NOT_FOUND", status=404)

    data = request.get_json(silent=True) or {}
    current_password = data.get("current_password") or ""
    new_password = data.get("new_password") or ""

    if not current_password or not new_password:
        return _err("Both current and new password are required.")

    if not user.check_password(current_password):
        return _err("Incorrect current password.", code="INVALID_PASSWORD", status=400)

    if err := _validate_password(new_password):
        return _err(err)

    user.set_password(new_password)
    db.session.commit()
    logger.info(f"Password changed for user: {user.email}")

    return _ok({"message": "Password changed successfully."})
