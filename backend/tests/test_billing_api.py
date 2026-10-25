from datetime import datetime, timedelta, timezone

import pytest

from app import create_app
from app.api import billing as billing_api
from app.config import Config
from app.models.billing import BillingEvent, Subscription, db
from app.models.user import User
from app.services.entitlements import get_entitlement


@pytest.fixture
def app_instance(tmp_path):
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path}/billing_api.db"
        JWT_SECRET_KEY = "test-jwt-secret-key-123456"
        RAZORPAY_KEY_ID = None
        RAZORPAY_KEY_SECRET = None
        RAZORPAY_WEBHOOK_SECRET = None
        RAZORPAY_PLAN_ID_STARTER_MONTHLY = None
        RAZORPAY_PLAN_ID_STARTER_ANNUAL = None
        RAZORPAY_PLAN_ID_PRO_MONTHLY = None
        RAZORPAY_PLAN_ID_PRO_ANNUAL = None
        RAZORPAY_PLAN_ID_PREMIUM_MONTHLY = None
        RAZORPAY_PLAN_ID_PREMIUM_ANNUAL = None

    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def _register(client, email="billing@example.com"):
    from unittest.mock import patch

    with patch("app.services.email_service.send_verification_email", return_value=True):
        response = client.post(
            "/api/auth/register",
            json={
                "email": email,
                "password": "Password123!",
                "full_name": "Billing Tester",
            },
        )
    data = response.get_json()
    user = db.session.get(User, data["user"]["id"])
    user.is_verified = True
    db.session.commit()
    return data["access_token"], user


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def _configure_razorpay(monkeypatch):
    monkeypatch.setattr(Config, "RAZORPAY_KEY_ID", "rzp_test_key")
    monkeypatch.setattr(Config, "RAZORPAY_KEY_SECRET", "rzp_test_secret")
    monkeypatch.setattr(Config, "RAZORPAY_WEBHOOK_SECRET", "whsec_test")
    for plan in ("STARTER", "PRO", "PREMIUM"):
        for interval in ("MONTHLY", "ANNUAL"):
            monkeypatch.setattr(
                Config, f"RAZORPAY_PLAN_ID_{plan}_{interval}", f"plan_{plan}_{interval}"
            )


def _local_subscription(user, **overrides):
    now = datetime.now(timezone.utc)
    values = {
        "user_id": user.id,
        "provider": "razorpay",
        "provider_subscription_id": "sub_test_123",
        "plan": "starter",
        "billing_interval": "monthly",
        "status": "created",
        "current_period_start": now,
        "current_period_end": now + timedelta(days=30),
    }
    values.update(overrides)
    subscription = Subscription(**values)
    db.session.add(subscription)
    db.session.commit()
    return subscription


def test_plans_endpoint_is_public_and_has_three_tiers(app_instance):
    client = app_instance.test_client()
    response = client.get("/api/billing/plans")

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["currency"] == "USD"
    assert [plan["id"] for plan in data["plans"]] == ["starter", "pro", "premium"]
    starter = data["plans"][0]
    assert starter["monthly_cents"] == 900
    assert starter["annual_cents"] == 9000
    assert starter["limits"]["max_rounds"] == 15
    assert data["configured"] is False


def test_me_returns_free_entitlement(app_instance):
    client = app_instance.test_client()
    token, _ = _register(client)
    response = client.get("/api/billing/me", headers=_auth(token))

    assert response.status_code == 200
    entitlement = response.get_json()["entitlement"]
    assert entitlement["plan"] == "free"
    assert entitlement["runs_limit"] == 1
    assert entitlement["configured"] is False


def test_subscribe_reports_unconfigured_billing(app_instance):
    client = app_instance.test_client()
    token, _ = _register(client)
    response = client.post(
        "/api/billing/subscribe",
        headers=_auth(token),
        json={"plan": "starter", "interval": "monthly"},
    )
    assert response.status_code == 503
    assert response.get_json()["code"] == "BILLING_NOT_CONFIGURED"


def test_subscribe_rejects_unknown_plan(app_instance):
    client = app_instance.test_client()
    token, _ = _register(client)
    response = client.post(
        "/api/billing/subscribe",
        headers=_auth(token),
        json={"plan": "enterprise", "interval": "monthly"},
    )
    assert response.status_code == 400
    assert response.get_json()["code"] == "INVALID_PLAN"


def test_subscribe_creates_local_pending_subscription(app_instance, monkeypatch):
    _configure_razorpay(monkeypatch)
    client = app_instance.test_client()
    token, user = _register(client)
    monkeypatch.setattr(
        billing_api.razorpay_service,
        "create_subscription",
        lambda user, plan, interval: {
            "id": "sub_test_123",
            "status": "created",
            "current_start": None,
            "current_end": None,
        },
    )

    response = client.post(
        "/api/billing/subscribe",
        headers=_auth(token),
        json={"plan": "starter", "interval": "monthly"},
    )
    assert response.status_code == 201
    payload = response.get_json()
    assert payload["subscription_id"] == "sub_test_123"
    assert payload["key_id"] == "rzp_test_key"

    subscription = Subscription.query.filter_by(user_id=user.id).one()
    assert subscription.status == "created"
    assert subscription.plan == "starter"


def test_verify_activates_subscription(app_instance, monkeypatch):
    _configure_razorpay(monkeypatch)
    client = app_instance.test_client()
    token, user = _register(client)
    _local_subscription(user)
    now = int(datetime.now(timezone.utc).timestamp())

    monkeypatch.setattr(
        billing_api.razorpay_service, "verify_checkout_signature", lambda *args: True
    )
    monkeypatch.setattr(
        billing_api.razorpay_service,
        "fetch_subscription",
        lambda subscription_id: {
            "id": subscription_id,
            "status": "active",
            "current_start": now,
            "current_end": now + 30 * 86400,
        },
    )

    response = client.post(
        "/api/billing/verify",
        headers=_auth(token),
        json={
            "razorpay_payment_id": "pay_123",
            "razorpay_subscription_id": "sub_test_123",
            "razorpay_signature": "sig",
        },
    )
    assert response.status_code == 200
    entitlement = response.get_json()["entitlement"]
    assert entitlement["plan"] == "starter"
    assert entitlement["runs_limit"] == 3
    assert entitlement["can_start"] is True


def test_verify_rejects_bad_signature(app_instance, monkeypatch):
    _configure_razorpay(monkeypatch)
    client = app_instance.test_client()
    token, user = _register(client)
    _local_subscription(user)
    monkeypatch.setattr(
        billing_api.razorpay_service, "verify_checkout_signature", lambda *args: False
    )

    response = client.post(
        "/api/billing/verify",
        headers=_auth(token),
        json={
            "razorpay_payment_id": "pay_123",
            "razorpay_subscription_id": "sub_test_123",
            "razorpay_signature": "bad",
        },
    )
    assert response.status_code == 400
    assert response.get_json()["code"] == "INVALID_SIGNATURE"


def test_webhook_activates_and_is_idempotent(app_instance, monkeypatch):
    _configure_razorpay(monkeypatch)
    client = app_instance.test_client()
    token, user = _register(client)
    _local_subscription(user)
    monkeypatch.setattr(
        billing_api.razorpay_service, "verify_webhook_signature", lambda *args: True
    )

    now = int(datetime.now(timezone.utc).timestamp())
    event = {
        "event": "subscription.activated",
        "payload": {
            "subscription": {
                "entity": {
                    "id": "sub_test_123",
                    "status": "active",
                    "current_start": now,
                    "current_end": now + 30 * 86400,
                    "plan_id": "plan_STARTER_MONTHLY",
                }
            }
        },
    }

    headers = {"X-Razorpay-Signature": "sig", "x-razorpay-event-id": "evt_1"}
    first = client.post("/api/billing/webhook", json=event, headers=headers)
    assert first.status_code == 200

    subscription = Subscription.query.filter_by(
        provider_subscription_id="sub_test_123"
    ).one()
    assert subscription.status == "active"
    assert subscription.current_period_end is not None

    second = client.post("/api/billing/webhook", json=event, headers=headers)
    assert second.status_code == 200
    assert BillingEvent.query.count() == 1
    assert get_entitlement(user)["can_start"] is True


def test_webhook_rejects_bad_signature(app_instance, monkeypatch):
    _configure_razorpay(monkeypatch)
    client = app_instance.test_client()
    monkeypatch.setattr(
        billing_api.razorpay_service, "verify_webhook_signature", lambda *args: False
    )
    response = client.post(
        "/api/billing/webhook",
        json={"event": "subscription.activated"},
        headers={"X-Razorpay-Signature": "bad"},
    )
    assert response.status_code == 400


def test_cancel_keeps_access_until_period_end(app_instance, monkeypatch):
    _configure_razorpay(monkeypatch)
    client = app_instance.test_client()
    token, user = _register(client)
    _local_subscription(user, status="active")
    monkeypatch.setattr(
        billing_api.razorpay_service,
        "cancel_subscription",
        lambda subscription_id: {"id": subscription_id, "status": "active"},
    )

    response = client.post("/api/billing/cancel", headers=_auth(token))
    assert response.status_code == 200
    assert response.get_json()["cancel_at_period_end"] is True

    subscription = Subscription.query.filter_by(user_id=user.id).one()
    assert subscription.cancel_at_period_end is True
    assert get_entitlement(user)["can_start"] is True
