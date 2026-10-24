"""
Brain Auth API — /api/auth/*
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
import threading
import traceback
from datetime import datetime, timezone

import bcrypt

from flask import Blueprint, request, jsonify, g

from ..config import Config
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

logger = logging.getLogger("brain.api.auth")

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
    full_name = (data.get("full_name") or data.get("name") or "").strip()

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

    try:
        # Create user
        user = User(email=email, full_name=full_name)
        user.set_password(password)
        if email in Config.admin_emails():
            user.role = "admin"
        token = user.generate_verification_token(ttl_hours=24)

        db.session.add(user)
        db.session.commit()

        logger.info(f"New user registered: {email} (id={user.id})")

        # Send verification email asynchronously in background so register returns immediately
        def _send_email_async():
            try:
                send_verification_email(email, full_name, token)
            except Exception as e:
                logger.error(f"Async email send failed for {email}: {e}")

        threading.Thread(target=_send_email_async, daemon=True).start()

        # Issue tokens immediately — user can explore, but sim features need verification
        t_ver = getattr(user, "token_version", 1)
        access = create_access_token(user.id, is_verified=False, token_version=t_ver)
        refresh = create_refresh_token(user.id, token_version=t_ver)

        return _ok({
            "message": "Account created! A 6-digit verification code has been sent to your email.",
            "access_token": access,
            "refresh_token": refresh,
            "user": user.to_public_dict(),
            "email_sent": True,
        }, status=201)
    except Exception as e:
        db.session.rollback()
        logger.error(f"Registration failed for {email}: {e}\n{traceback.format_exc()}")
        return _err(f"Registration failed: {str(e)}", status=500)


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

    # Constant-time comparison to prevent user enumeration via timing attack
    _DUMMY_BCRYPT = "$2b$12$e8rGg6eH.D3l5wM.0tT6tOOi7XkS0Qn6fS8YkH3QxTz3r1nZ9O9re"
    is_valid = user.check_password(password) if user else bcrypt.checkpw(password.encode(), _DUMMY_BCRYPT.encode())
    if not user or not is_valid:
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

    # Update last login and keep the operator allowlist authoritative
    user.last_login_at = datetime.now(timezone.utc)
    if user.email in Config.admin_emails() and user.role != "admin":
        user.role = "admin"
    db.session.commit()

    logger.info(f"User logged in: {email} (verified={user.is_verified})")

    t_ver = getattr(user, "token_version", 1)
    access = create_access_token(user.id, is_verified=user.is_verified, token_version=t_ver)
    refresh = create_refresh_token(user.id, token_version=t_ver)

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

    # Verify token version to support server-side logout and session invalidation
    token_v = payload.get("v")
    user_v = getattr(user, "token_version", 1)
    if token_v is not None and token_v != user_v:
        return _err("Session has been revoked. Please log in again.", code="TOKEN_REVOKED", status=401)

    new_access = create_access_token(user.id, is_verified=user.is_verified, token_version=user_v)
    new_refresh = create_refresh_token(user.id, token_version=user_v)
    return _ok({
        "access_token": new_access,
        "refresh_token": new_refresh,
        "user": user.to_public_dict(),
    })


# ------------------------------------------------------------------ #
# POST /api/auth/verify-email or POST /api/auth/verify-otp
# ------------------------------------------------------------------ #

@auth_bp.route("/verify-email", methods=["GET", "POST"])
@auth_bp.route("/verify-otp", methods=["POST"])
def verify_email():
    """
    Verify a user's email address using a 6-digit OTP code (or token).

    JSON body or Query params: { email?: string, otp?: string, token?: string }

    On success: marks user as verified, sends welcome email, returns
    fresh access token with is_verified=True so the frontend can update state.
    """
    data = request.get_json(silent=True) or {}
    code = (data.get("otp") or data.get("token") or request.args.get("otp") or request.args.get("token") or "").strip()
    email = (data.get("email") or request.args.get("email") or "").strip().lower()

    if not code:
        return _err("Verification code is required.", code="MISSING_CODE")

    # If email provided, find by email; otherwise find by token
    if email:
        user = User.query.filter_by(email=email).first()
    else:
        user = User.query.filter_by(verification_token=code).first()

    if not user:
        return _err(
            "This verification code is invalid or has already been used.",
            code="CODE_INVALID"
        )

    if user.is_verified:
        t_ver = getattr(user, "token_version", 1)
        new_access = create_access_token(user.id, is_verified=True, token_version=t_ver)
        return _ok({
            "message": "Your email is already verified. You're all set!",
            "access_token": new_access,
            "user": user.to_public_dict(),
        })

    if user.is_verification_token_expired():
        return _err(
            "This verification code has expired. Please request a new one.",
            code="CODE_EXPIRED"
        )

    # Verify matching OTP code
    if not user.verify_email(code):
        return _err("Invalid verification code. Please check your email and try again.", code="VERIFICATION_FAILED")

    db.session.commit()
    logger.info(f"Email verified via OTP: {user.email}")

    # Send welcome email asynchronously
    try:
        send_welcome_email(user.email, user.full_name)
    except Exception as e:
        logger.warning(f"Welcome email error for {user.email}: {e}")

    # Return updated access token so frontend can reflect verified state immediately
    t_ver = getattr(user, "token_version", 1)
    new_access = create_access_token(user.id, is_verified=True, token_version=t_ver)

    return _ok({
        "message": "Email verified successfully! Welcome to Brain.",
        "access_token": new_access,
        "user": user.to_public_dict(),
    })


# ------------------------------------------------------------------ #
# POST /api/auth/resend-verification
# ------------------------------------------------------------------ #

@auth_bp.route("/resend-verification", methods=["POST"])
def resend_verification():
    """
    Re-send the 6-digit OTP verification email.

    Body: { email }
    """
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()

    if not email:
        return _err("Email address is required.")

    user = User.query.filter_by(email=email).first()

    # Always return the same response to prevent user enumeration
    generic_ok = _ok({
        "message": "If an unverified account exists with that email, a new 6-digit verification code has been sent."
    })

    if not user or user.is_verified:
        return generic_ok

    otp = user.generate_verification_otp(ttl_minutes=15)
    db.session.commit()

    def _send_otp_async():
        try:
            send_verification_email(user.email, user.full_name, otp)
        except Exception as e:
            logger.error(f"Failed to resend verification OTP to {user.email}: {e}")

    threading.Thread(target=_send_otp_async, daemon=True).start()

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

    user.token_version = (getattr(user, "token_version", 1) or 1) + 1
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
# PUT /api/auth/profile (Update name)
# ------------------------------------------------------------------ #

@auth_bp.route("/profile", methods=["PUT", "PATCH"])
@require_auth
def update_profile():
    """Update editable profile fields.

    Body: { full_name? }
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
    user.token_version = (getattr(user, "token_version", 1) or 1) + 1
    db.session.commit()
    logger.info(f"Password changed for user: {user.email}")

    return _ok({"message": "Password changed successfully."})


# ------------------------------------------------------------------ #
# POST /api/auth/logout
# ------------------------------------------------------------------ #

@auth_bp.route("/logout", methods=["POST"])
@require_auth
def logout():
    """
    Server-side logout: Invalidates all refresh tokens for current user
    by incrementing token_version.
    Requires: valid access token.
    """
    user = db.session.get(User, g.user_id)
    if user:
        user.token_version = (getattr(user, "token_version", 1) or 1) + 1
        db.session.commit()
        logger.info(f"User logged out, session invalidated: {user.email}")

    return _ok({"message": "Successfully logged out."})

