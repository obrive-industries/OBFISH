"""
ObMind User Model
SQLAlchemy ORM model for user accounts.
Stores credentials, verification state, and profile info.
"""

import uuid
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_dt(dt: datetime | None) -> datetime | None:
    """Ensure datetime is timezone-aware (UTC) even if stored as naive in SQLite."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


class User(db.Model):
    """User account model."""

    __tablename__ = "users"

    # Primary identity
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(255), nullable=False)

    # Auth
    password_hash = db.Column(db.String(255), nullable=False)

    # Email verification
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    verification_token = db.Column(db.String(64), nullable=True, index=True)
    verification_token_expires_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Password reset
    reset_token = db.Column(db.String(64), nullable=True, index=True)
    reset_token_expires_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Account state
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=_utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow)
    last_login_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # BYOK (Bring Your Own Key) Settings
    custom_llm_api_key = db.Column(db.String(255), nullable=True)
    custom_llm_base_url = db.Column(db.String(255), nullable=True)
    custom_llm_model_name = db.Column(db.String(255), nullable=True)

    # ------------------------------------------------------------------ #
    # Password helpers
    # ------------------------------------------------------------------ #

    def set_password(self, plaintext: str) -> None:
        """Hash and store password using bcrypt (cost factor 12)."""
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(plaintext.encode(), salt).decode()

    def check_password(self, plaintext: str) -> bool:
        """Verify a plaintext password against the stored hash."""
        return bcrypt.checkpw(plaintext.encode(), self.password_hash.encode())

    # ------------------------------------------------------------------ #
    # Email verification
    # ------------------------------------------------------------------ #

    def generate_verification_token(self, ttl_hours: int = 24) -> str:
        """Create a secure URL-safe token for email verification."""
        token = secrets.token_urlsafe(48)
        self.verification_token = token
        self.verification_token_expires_at = _utcnow() + timedelta(hours=ttl_hours)
        return token

    def verify_email(self, token: str) -> bool:
        """
        Validate the email verification token.
        Returns True and marks the account verified if the token is valid and unexpired.
        """
        if not self.verification_token:
            return False
        if self.verification_token != token:
            return False
        exp = _normalize_dt(self.verification_token_expires_at)
        if exp and _utcnow() > exp:
            return False  # Token expired

        self.is_verified = True
        self.verification_token = None
        self.verification_token_expires_at = None
        return True

    def is_verification_token_expired(self) -> bool:
        if not self.verification_token_expires_at:
            return True
        exp = _normalize_dt(self.verification_token_expires_at)
        return _utcnow() > exp if exp else True

    # ------------------------------------------------------------------ #
    # Password reset
    # ------------------------------------------------------------------ #

    def generate_reset_token(self, ttl_minutes: int = 30) -> str:
        """Create a secure token for password reset (short TTL)."""
        token = secrets.token_urlsafe(48)
        self.reset_token = token
        self.reset_token_expires_at = _utcnow() + timedelta(minutes=ttl_minutes)
        return token

    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Validate reset token, set new password, and invalidate the token.
        Returns True on success.
        """
        if not self.reset_token:
            return False
        if self.reset_token != token:
            return False
        exp = _normalize_dt(self.reset_token_expires_at)
        if exp and _utcnow() > exp:
            return False  # Token expired

        self.set_password(new_password)
        self.reset_token = None
        self.reset_token_expires_at = None
        return True

    # ------------------------------------------------------------------ #
    # Serialisation
    # ------------------------------------------------------------------ #

    def to_public_dict(self) -> dict:
        """Safe dict — never includes password hash or tokens."""
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "has_custom_api_key": bool(self.custom_llm_api_key),
            "custom_llm_base_url": self.custom_llm_base_url,
            "custom_llm_model_name": self.custom_llm_model_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }

    def __repr__(self) -> str:
        return f"<User {self.email} verified={self.is_verified}>"
