import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app import create_app
from app.config import Config
from app.models.billing import Subscription, UsageEvent, db
from app.models.user import User
from app.services.entitlements import (
    active_plan_denial,
    clamp_rounds,
    deny_reason,
    get_entitlement,
    record_run,
)


@pytest.fixture
def app_ctx(tmp_path):
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path}/billing.db"
        JWT_SECRET_KEY = "test-jwt-secret-key-123456"

    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def _user(email="plan@example.com", role="user"):
    user = User(email=email, full_name="Plan Tester", role=role)
    user.set_password("Password123!")
    user.is_verified = True
    db.session.add(user)
    db.session.commit()
    return user


def _subscription(user, plan="starter", interval="monthly", status="active", days=30):
    now = datetime.now(timezone.utc)
    subscription = Subscription(
        user_id=user.id,
        provider="manual",
        provider_subscription_id=f"sub_{uuid.uuid4().hex}",
        plan=plan,
        billing_interval=interval,
        status=status,
        current_period_start=now - timedelta(days=1),
        current_period_end=now + timedelta(days=days),
    )
    db.session.add(subscription)
    db.session.commit()
    return subscription


def test_free_user_gets_one_demo_run(app_ctx):
    user = _user("free@example.com")
    entitlement = get_entitlement(user)

    assert entitlement["plan"] == "free"
    assert entitlement["runs_limit"] == 1
    assert entitlement["runs_used"] == 0
    assert entitlement["max_rounds"] == 10
    assert entitlement["can_start"] is True
    assert deny_reason(user, entitlement) is None
    assert active_plan_denial(user) is None
    assert clamp_rounds(user, 15) == 10

    # Consumes the 1 free demo run:
    assert record_run(user, "proj_free_1") is True
    # Idempotent call on same project succeeds:
    assert record_run(user, "proj_free_1") is True
    # Authorized to continue working on that project:
    assert active_plan_denial(user, "proj_free_1") is None

    # After using the 1 free run:
    entitlement_after = get_entitlement(user)
    assert entitlement_after["runs_used"] == 1
    assert entitlement_after["can_start"] is False
    assert deny_reason(user, entitlement_after)[0] == "PLAN_REQUIRED"

    # Second project cannot be started:
    assert record_run(user, "proj_free_2") is False
    assert active_plan_denial(user, "proj_free_2")[0] == "PLAN_REQUIRED"


def test_admin_is_unlimited(app_ctx):
    user = _user("admin@example.com", role="admin")
    entitlement = get_entitlement(user)

    assert entitlement["is_admin"] is True
    assert entitlement["unlimited"] is True
    assert entitlement["max_rounds"] is None
    assert active_plan_denial(user) is None
    assert record_run(user, "proj_admin") is True


def test_admin_via_env_email(app_ctx, monkeypatch):
    monkeypatch.setattr(Config, "ADMIN_EMAILS_ENV", "env_admin@example.com, other@example.com")
    user = _user("env_admin@example.com", role="user")
    entitlement = get_entitlement(user)

    assert entitlement["is_admin"] is True
    assert entitlement["unlimited"] is True
    assert entitlement["max_rounds"] is None
    assert active_plan_denial(user) is None
    assert record_run(user, "proj_env_admin") is True


def test_starter_limits_and_idempotent_consumption(app_ctx):
    user = _user("starter@example.com")
    _subscription(user, plan="starter", interval="monthly")

    entitlement = get_entitlement(user)
    assert entitlement["runs_limit"] == 3
    assert entitlement["max_rounds"] == 15
    assert entitlement["can_start"] is True
    assert clamp_rounds(user, 50) == 15
    assert clamp_rounds(user, 4) == 4
    assert clamp_rounds(user, None) == 15

    assert record_run(user, "proj_1") is True
    assert record_run(user, "proj_1") is True
    assert record_run(user, "proj_2") is True
    assert record_run(user, "proj_3") is True
    assert get_entitlement(user)["runs_used"] == 3
    assert record_run(user, "proj_4") is False
    assert deny_reason(user, get_entitlement(user))[0] == "PLAN_LIMIT_REACHED"


def test_annual_allotment_and_round_cap(app_ctx):
    user = _user("annual@example.com")
    _subscription(user, plan="pro", interval="annual")

    entitlement = get_entitlement(user)
    assert entitlement["runs_limit"] == 120
    assert entitlement["max_rounds"] == 40
    assert clamp_rounds(user, 100) == 40


def test_usage_outside_period_is_ignored(app_ctx):
    user = _user("rollover@example.com")
    subscription = _subscription(user, plan="starter", interval="monthly")
    subscription.current_period_start = datetime.now(timezone.utc) - timedelta(days=5)
    db.session.commit()

    db.session.add(
        UsageEvent(
            user_id=user.id,
            kind="run",
            ref_id="old_project",
            created_at=datetime.now(timezone.utc) - timedelta(days=40),
        )
    )
    db.session.commit()

    assert get_entitlement(user)["runs_used"] == 0
    assert record_run(user, "new_project") is True
    assert get_entitlement(user)["runs_used"] == 1


def test_halted_subscription_blocks_and_cancelled_keeps_access(app_ctx):
    halted_user = _user("halted@example.com")
    _subscription(halted_user, status="halted")
    assert active_plan_denial(halted_user)[0] == "PLAN_PAST_DUE"
    assert get_entitlement(halted_user)["can_start"] is False

    cancelled_user = _user("cancelled@example.com")
    _subscription(cancelled_user, plan="pro", status="cancelled")
    entitlement = get_entitlement(cancelled_user)
    assert entitlement["plan"] == "pro"
    assert entitlement["can_start"] is True
    assert active_plan_denial(cancelled_user) is None
