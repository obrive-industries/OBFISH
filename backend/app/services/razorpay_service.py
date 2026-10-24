"""Thin Razorpay subscription wrapper.

All prices are chosen server-side from the plan catalog; the browser only ever
receives a subscription id and the publishable key id.
"""

from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timezone
from typing import Any

from ..billing.catalog import get_razorpay_plan_id
from ..config import Config


class BillingError(RuntimeError):
    """Raised when billing is unavailable or the provider rejects a request."""

    def __init__(self, message: str, code: str = "BILLING_PROVIDER_ERROR", status: int = 502):
        super().__init__(message)
        self.code = code
        self.status = status


TOTAL_COUNT = {"monthly": 120, "annual": 10}


def _client():
    if not Config.RAZORPAY_KEY_ID or not Config.RAZORPAY_KEY_SECRET:
        raise BillingError(
            "Billing is not configured yet.",
            code="BILLING_NOT_CONFIGURED",
            status=503,
        )
    try:
        import razorpay
    except ImportError as exc:  # pragma: no cover - dependency guard
        raise BillingError(
            "Razorpay SDK is not installed.",
            code="BILLING_NOT_CONFIGURED",
            status=503,
        ) from exc
    return razorpay.Client(auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET))


def create_subscription(user, plan_id: str, interval: str) -> dict[str, Any]:
    razorpay_plan_id = get_razorpay_plan_id(plan_id, interval)
    if not razorpay_plan_id:
        raise BillingError(
            "This plan is not available for checkout yet.",
            code="BILLING_NOT_CONFIGURED",
            status=503,
        )
    payload = {
        "plan_id": razorpay_plan_id,
        "total_count": TOTAL_COUNT.get(interval, 12),
        "quantity": 1,
        "customer_notify": 1,
        "notes": {
            "user_id": str(user.id),
            "email": user.email,
            "plan": plan_id,
            "interval": interval,
        },
    }
    try:
        return _client().subscription.create(payload)
    except BillingError:
        raise
    except Exception as exc:
        raise BillingError(f"Could not start checkout: {exc}") from exc


def fetch_subscription(subscription_id: str) -> dict[str, Any]:
    try:
        return _client().subscription.fetch(subscription_id)
    except BillingError:
        raise
    except Exception as exc:
        raise BillingError(f"Could not load the subscription: {exc}") from exc


def cancel_subscription(subscription_id: str) -> dict[str, Any]:
    try:
        return _client().subscription.cancel(
            subscription_id, {"cancel_at_cycle_end": 1}
        )
    except BillingError:
        raise
    except Exception as exc:
        raise BillingError(f"Could not cancel the subscription: {exc}") from exc


def verify_checkout_signature(
    payment_id: str, subscription_id: str, signature: str
) -> bool:
    if not (
        Config.RAZORPAY_KEY_SECRET
        and payment_id
        and subscription_id
        and signature
    ):
        return False
    message = f"{payment_id}|{subscription_id}".encode("utf-8")
    expected = hmac.new(
        Config.RAZORPAY_KEY_SECRET.encode("utf-8"), message, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def verify_webhook_signature(raw_body: bytes | str, signature: str) -> bool:
    if not (Config.RAZORPAY_WEBHOOK_SECRET and signature):
        return False
    try:
        _client().utility.verify_webhook_signature(
            raw_body, signature, Config.RAZORPAY_WEBHOOK_SECRET
        )
        return True
    except BillingError:
        raise
    except Exception:
        return False


def epoch_to_datetime(value: Any) -> datetime | None:
    if value in (None, "", 0):
        return None
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None
