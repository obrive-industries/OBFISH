"""Billing persistence: subscriptions, usage consumption and webhook receipts."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from .user import db


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def as_aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


class Subscription(db.Model):
    """One Razorpay subscription per account, updated by signed webhooks."""

    __tablename__ = "billing_subscriptions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    provider = db.Column(db.String(32), nullable=False, default="razorpay")
    provider_subscription_id = db.Column(db.String(128), nullable=False, unique=True, index=True)
    plan = db.Column(db.String(32), nullable=False)
    billing_interval = db.Column(db.String(16), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="created")
    current_period_start = db.Column(db.DateTime(timezone=True), nullable=True)
    current_period_end = db.Column(db.DateTime(timezone=True), nullable=True)
    cancel_at_period_end = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow
    )

    def __repr__(self) -> str:
        return f"<Subscription {self.plan}/{self.billing_interval} {self.status}>"


class UsageEvent(db.Model):
    """A consumed run. `ref_id` makes consumption idempotent per project."""

    __tablename__ = "billing_usage_events"
    __table_args__ = (
        db.UniqueConstraint("user_id", "kind", "ref_id", name="uq_usage_user_kind_ref"),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    kind = db.Column(db.String(32), nullable=False, default="run")
    ref_id = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)


class BillingEvent(db.Model):
    """Idempotency ledger for webhook deliveries."""

    __tablename__ = "billing_events"

    event_id = db.Column(db.String(128), primary_key=True)
    event_type = db.Column(db.String(64), nullable=False)
    received_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
