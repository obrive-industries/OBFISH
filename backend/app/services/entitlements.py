"""Plan entitlement checks shared by every cost-bearing API route."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy.exc import IntegrityError

from ..billing.catalog import PLAN_BY_ID
from ..models.billing import Subscription, UsageEvent, as_aware, db


UNLIMITED = None
ACCESS_STATUSES = {"active", "cancelled", "completed"}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def get_latest_subscription(user_id: str) -> Subscription | None:
    return (
        Subscription.query.filter_by(user_id=user_id)
        .order_by(Subscription.created_at.desc())
        .first()
    )


def _active_subscription(user_id: str) -> Subscription | None:
    subscription = get_latest_subscription(user_id)
    if not subscription:
        return None
    period_end = as_aware(subscription.current_period_end)
    if subscription.status not in ACCESS_STATUSES or period_end is None:
        return None
    if period_end <= _now():
        return None
    return subscription


def _count_runs(user_id: str, start: datetime | None, end: datetime | None) -> int:
    query = UsageEvent.query.filter_by(user_id=user_id, kind="run")
    if start is not None:
        query = query.filter(UsageEvent.created_at >= start)
    if end is not None:
        query = query.filter(UsageEvent.created_at < end)
    return query.count()


def get_entitlement(user: Any | None) -> dict[str, Any]:
    """Return the effective plan, usage and limits for a user."""

    free = {
        "plan": "free",
        "plan_name": "Free demo",
        "status": "none",
        "interval": None,
        "is_admin": False,
        "configured": False,
        "runs_used": 0,
        "runs_limit": 0,
        "max_rounds": UNLIMITED,
        "period_start": None,
        "period_end": None,
        "renews_at": None,
        "cancel_at_period_end": False,
        "can_start": False,
        "unlimited": False,
    }
    if user is None:
        return free

    if getattr(user, "role", "user") == "admin":
        return {
            **free,
            "plan": "admin",
            "plan_name": "Admin",
            "status": "active",
            "is_admin": True,
            "runs_limit": UNLIMITED,
            "max_rounds": UNLIMITED,
            "can_start": True,
            "unlimited": True,
        }

    subscription = _active_subscription(user.id)
    if not subscription:
        latest = get_latest_subscription(user.id)
        if latest is not None:
            free["status"] = latest.status
            free["plan"] = latest.plan
            free["interval"] = latest.billing_interval
        return free

    plan = PLAN_BY_ID.get(subscription.plan)
    if plan is None:
        return free

    period_start = as_aware(subscription.current_period_start)
    period_end = as_aware(subscription.current_period_end)
    interval = subscription.billing_interval
    runs_limit = int(plan["limits"]["runs_per_period"].get(interval, 0))
    runs_used = _count_runs(user.id, period_start, period_end)

    return {
        **free,
        "plan": plan["id"],
        "plan_name": plan["name"],
        "status": subscription.status,
        "interval": interval,
        "runs_used": runs_used,
        "runs_limit": runs_limit,
        "max_rounds": int(plan["limits"]["max_rounds"]),
        "period_start": period_start.isoformat() if period_start else None,
        "period_end": period_end.isoformat() if period_end else None,
        "renews_at": period_end.isoformat() if period_end else None,
        "cancel_at_period_end": bool(subscription.cancel_at_period_end),
        "can_start": runs_used < runs_limit,
    }


def active_plan_denial(user: Any | None) -> tuple[str, str] | None:
    """Return (code, message) when the account has no usable paid plan."""

    if user is None:
        return "MISSING_TOKEN", "Authentication required. Please sign in to run simulations."
    if not getattr(user, "is_verified", False):
        return "EMAIL_NOT_VERIFIED", "Please verify your email address before running simulations."

    entitlement = get_entitlement(user)
    if entitlement.get("unlimited"):
        return None
    status = entitlement.get("status")
    if status in {"pending", "halted"}:
        return "PLAN_PAST_DUE", (
            "Your subscription payment needs attention. Update billing to continue."
        )
    if entitlement.get("plan") == "free" or not entitlement.get("period_end"):
        return "PLAN_REQUIRED", (
            "An active plan is required to run your own simulations. "
            "Explore the sample report, then choose a plan to continue."
        )
    return None


def deny_reason(user: Any | None, entitlement: dict[str, Any]) -> tuple[str, str] | None:
    """Return (code, message) when the user may not start a new run."""

    denied = active_plan_denial(user)
    if denied:
        return denied
    if entitlement.get("unlimited"):
        return None
    if not entitlement.get("can_start"):
        return "PLAN_LIMIT_REACHED", (
            "You have used every simulation run included in this billing period. "
            "Upgrade your plan or wait for the next period."
        )
    return None


def record_run(user: Any | None, project_id: str) -> bool:
    """Consume one run for a project, idempotently. False when over quota."""

    if user is None or not project_id:
        return False
    if getattr(user, "role", "user") == "admin":
        return True

    entitlement = get_entitlement(user)
    if entitlement.get("unlimited") or not entitlement.get("period_end"):
        return bool(entitlement.get("unlimited"))

    existing = UsageEvent.query.filter_by(
        user_id=user.id, kind="run", ref_id=project_id
    ).first()
    if existing:
        return True

    if not entitlement.get("can_start"):
        return False

    db.session.add(UsageEvent(user_id=user.id, kind="run", ref_id=project_id))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return True

    # A concurrent request may have slipped past the pre-check. Keep the
    # ledger honest by removing the overflow row.
    fresh = get_entitlement(user)
    if fresh.get("runs_used", 0) > fresh.get("runs_limit", 0):
        UsageEvent.query.filter_by(
            user_id=user.id, kind="run", ref_id=project_id
        ).delete(synchronize_session=False)
        db.session.commit()
        return False
    return True


def clamp_rounds(user: Any | None, requested: int | None) -> int | None:
    """Cap a requested round count at the plan limit."""

    if user is None:
        return requested
    limit = get_entitlement(user).get("max_rounds")
    if limit is None:
        return requested
    if requested is None or requested <= 0:
        return int(limit)
    return min(int(requested), int(limit))
