"""Subscription billing endpoints backed by Razorpay."""

from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request

from ..billing.catalog import (
    PLAN_BY_ID,
    billing_configured,
    plan_from_razorpay_id,
    public_catalog,
)
from ..config import Config
from ..models.billing import BillingEvent, Subscription, as_aware, db
from ..services import razorpay_service
from ..services.entitlements import (
    _active_subscription,
    get_entitlement,
    get_latest_subscription,
)
from ..services.razorpay_service import BillingError, epoch_to_datetime
from ..utils.auth_middleware import get_current_user, require_auth
from ..utils.logger import get_logger

logger = get_logger("brain.api.billing")

billing_bp = Blueprint("billing", __name__)


def _ok(data: dict, status: int = 200):
    return jsonify({"success": True, **data}), status


def _err(message: str, code: str, status: int):
    return jsonify({"success": False, "error": message, "code": code}), status


def _entitlement_payload(user) -> dict:
    entitlement = get_entitlement(user)
    entitlement["configured"] = billing_configured()
    return entitlement


def _plan_payload(plan_id: str | None) -> dict | None:
    plan = PLAN_BY_ID.get(plan_id or "")
    if not plan:
        return None
    return {
        "id": plan["id"],
        "name": plan["name"],
        "badge": plan["badge"],
        "limits": plan["limits"],
        "cta": plan["cta"],
    }


@billing_bp.route("/plans", methods=["GET"])
def plans():
    return _ok({"data": public_catalog()})


@billing_bp.route("/me", methods=["GET"])
@require_auth
def me():
    user = get_current_user()
    if not user:
        return _err("User not found.", "USER_NOT_FOUND", 404)
    entitlement = _entitlement_payload(user)
    return _ok(
        {
            "entitlement": entitlement,
            "plan": _plan_payload(entitlement.get("plan")),
            "subscription": _subscription_payload(get_latest_subscription(user.id)),
        }
    )


def _subscription_payload(subscription: Subscription | None) -> dict | None:
    if subscription is None:
        return None
    period_end = as_aware(subscription.current_period_end)
    return {
        "id": subscription.id,
        "plan": subscription.plan,
        "interval": subscription.billing_interval,
        "status": subscription.status,
        "current_period_end": period_end.isoformat() if period_end else None,
        "cancel_at_period_end": bool(subscription.cancel_at_period_end),
    }


def _sync_subscription(subscription: Subscription, entity: dict) -> None:
    """Apply a Razorpay subscription entity to the local row."""

    status = (entity.get("status") or subscription.status or "").strip().lower()
    if status == "authenticated":
        # Checkout has captured the first payment; treat it as active access.
        status = "active"
    if status:
        subscription.status = status

    period_start = epoch_to_datetime(entity.get("current_start"))
    period_end = epoch_to_datetime(entity.get("current_end"))
    if period_end is None and status == "active":
        now = datetime.now(timezone.utc)
        days = 366 if subscription.billing_interval == "annual" else 31
        period_end = now + timedelta(days=days)
        period_start = period_start or now
    if period_start is not None:
        subscription.current_period_start = period_start
    if period_end is not None:
        subscription.current_period_end = period_end

    mapped = plan_from_razorpay_id(entity.get("plan_id"))
    if mapped:
        subscription.plan, subscription.billing_interval = mapped

    if "cancel_at_cycle_end" in entity:
        subscription.cancel_at_period_end = bool(entity.get("cancel_at_cycle_end"))
    db.session.commit()


@billing_bp.route("/subscribe", methods=["POST"])
@require_auth
def subscribe():
    user = get_current_user()
    if not user:
        return _err("User not found.", "USER_NOT_FOUND", 404)
    if not user.is_verified:
        return _err(
            "Please verify your email address before subscribing.",
            "EMAIL_NOT_VERIFIED",
            403,
        )
    data = request.get_json(silent=True) or {}
    plan_id = (data.get("plan") or "").strip().lower()
    interval = (data.get("interval") or "monthly").strip().lower()
    if plan_id not in PLAN_BY_ID:
        return _err("Unknown plan.", "INVALID_PLAN", 400)
    if interval not in {"monthly", "annual"}:
        return _err("Billing interval must be monthly or annual.", "INVALID_INTERVAL", 400)

    if not billing_configured():
        return _err(
            "Billing is not configured yet. Please try again later.",
            "BILLING_NOT_CONFIGURED",
            503,
        )

    if _active_subscription(user.id):
        return _err(
            "An active subscription already exists for this account.",
            "SUBSCRIPTION_EXISTS",
            409,
        )

    try:
        entity = razorpay_service.create_subscription(user, plan_id, interval)
    except BillingError as exc:
        return _err(str(exc), exc.code, exc.status)

    subscription_id = entity.get("id")
    if not subscription_id:
        return _err(
            "The payment provider did not return a subscription.",
            "BILLING_PROVIDER_ERROR",
            502,
        )

    subscription = Subscription(
        user_id=user.id,
        provider="razorpay",
        provider_subscription_id=subscription_id,
        plan=plan_id,
        billing_interval=interval,
        status=(entity.get("status") or "created").lower(),
        current_period_start=epoch_to_datetime(entity.get("current_start")),
        current_period_end=epoch_to_datetime(entity.get("current_end")),
    )
    db.session.add(subscription)
    db.session.commit()

    return _ok(
        {
            "key_id": Config.RAZORPAY_KEY_ID,
            "subscription_id": subscription_id,
            "prefill": {"name": user.full_name, "email": user.email},
        },
        status=201,
    )


@billing_bp.route("/verify", methods=["POST"])
@require_auth
def verify():
    user = get_current_user()
    if not user:
        return _err("User not found.", "USER_NOT_FOUND", 404)

    data = request.get_json(silent=True) or {}
    payment_id = (data.get("razorpay_payment_id") or "").strip()
    subscription_id = (data.get("razorpay_subscription_id") or "").strip()
    signature = (data.get("razorpay_signature") or "").strip()

    subscription = Subscription.query.filter_by(
        user_id=user.id, provider_subscription_id=subscription_id
    ).first()
    if not subscription:
        return _err("Unknown subscription.", "SUBSCRIPTION_NOT_FOUND", 404)

    if not razorpay_service.verify_checkout_signature(
        payment_id, subscription_id, signature
    ):
        return _err("Payment signature verification failed.", "INVALID_SIGNATURE", 400)

    try:
        entity = razorpay_service.fetch_subscription(subscription_id)
        _sync_subscription(subscription, entity)
    except BillingError as exc:
        # The signature proves the payment, so grant access on a provisional
        # period even when the follow-up fetch fails; the webhook reconciles it.
        logger.warning("Razorpay fetch after checkout failed: %s", exc)
        _sync_subscription(subscription, {"status": "active"})

    return _ok({"entitlement": _entitlement_payload(user)})


@billing_bp.route("/cancel", methods=["POST"])
@require_auth
def cancel():
    user = get_current_user()
    if not user:
        return _err("User not found.", "USER_NOT_FOUND", 404)

    subscription = _active_subscription(user.id)
    if not subscription:
        return _err("No active subscription found.", "SUBSCRIPTION_NOT_FOUND", 404)

    try:
        razorpay_service.cancel_subscription(subscription.provider_subscription_id)
    except BillingError as exc:
        return _err(str(exc), exc.code, exc.status)

    subscription.cancel_at_period_end = True
    db.session.commit()
    return _ok(
        {
            "cancel_at_period_end": True,
            "current_period_end": (
                as_aware(subscription.current_period_end).isoformat()
                if subscription.current_period_end
                else None
            ),
        }
    )


@billing_bp.route("/webhook", methods=["POST"])
def webhook():
    raw_body = request.get_data()
    signature = request.headers.get("X-Razorpay-Signature", "")
    if not razorpay_service.verify_webhook_signature(raw_body, signature):
        return _err("Invalid webhook signature.", "INVALID_SIGNATURE", 400)

    event = request.get_json(silent=True) or {}
    event_type = (event.get("event") or "").strip()
    event_id = request.headers.get("x-razorpay-event-id") or hashlib.sha256(
        raw_body
    ).hexdigest()

    if db.session.get(BillingEvent, event_id):
        return _ok({"received": True})

    payload = (event.get("payload") or {}).get("subscription") or {}
    entity = payload.get("entity") or {}
    subscription_id = entity.get("id")
    subscription = (
        Subscription.query.filter_by(provider_subscription_id=subscription_id).first()
        if subscription_id
        else None
    )

    if subscription is None:
        logger.warning("Webhook for unknown subscription: %s", subscription_id)
    elif event_type in {
        "subscription.activated",
        "subscription.authenticated",
        "subscription.charged",
        "subscription.pending",
        "subscription.halted",
        "subscription.cancelled",
        "subscription.completed",
    }:
        _sync_subscription(subscription, entity)

    db.session.add(BillingEvent(event_id=event_id, event_type=event_type or "unknown"))
    db.session.commit()
    return _ok({"received": True})
