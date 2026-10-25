"""
Tests for Wishlist API — /api/wishlist/*
Covers public subscription, duplicate handling, validation, and admin-only listing/export.
"""

import pytest
from app import create_app
from app.config import Config
from app.models.user import db, User
from app.models.wishlist import WishlistSubscriber
from app.utils.jwt_utils import create_access_token


@pytest.fixture
def app_and_client(tmp_path):
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path}/test_wishlist.db"
        JWT_SECRET_KEY = "test-jwt-secret-key-123456"

    app = create_app(TestConfig)
    client = app.test_client()

    with app.app_context():
        db.create_all()

        # Regular user
        user = User(email="regular@example.com", full_name="Regular User", role="user")
        user.set_password("Password123!")
        user.is_verified = True
        db.session.add(user)

        # Admin user
        admin = User(email="ai@obrive.com", full_name="Obrive Admin", role="admin")
        admin.set_password("AdminPass123!")
        admin.is_verified = True
        db.session.add(admin)

        db.session.commit()

        user_token = create_access_token(user.id, is_verified=True)
        admin_token = create_access_token(admin.id, is_verified=True)

        yield {
            "app": app,
            "client": client,
            "user_token": user_token,
            "admin_token": admin_token,
        }


def test_subscribe_success(app_and_client):
    client = app_and_client["client"]
    res = client.post("/api/wishlist/subscribe", json={
        "email": "innovator@company.io",
        "source": "landing_hero"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["already_subscribed"] is False
    assert "Thank you" in data["message"]

    # Verify persisted in database
    with app_and_client["app"].app_context():
        sub = WishlistSubscriber.query.filter_by(email="innovator@company.io").first()
        assert sub is not None
        assert sub.source == "landing_hero"
        assert sub.status == "active"


def test_subscribe_duplicate_case_insensitive(app_and_client):
    client = app_and_client["client"]
    # First subscription
    res1 = client.post("/api/wishlist/subscribe", json={"email": "alice@Startup.com"})
    assert res1.status_code == 201

    # Second subscription with different case
    res2 = client.post("/api/wishlist/subscribe", json={"email": "ALICE@startup.com"})
    assert res2.status_code == 200
    data = res2.get_json()
    assert data["success"] is True
    assert data["already_subscribed"] is True

    # Ensure only 1 record in database
    with app_and_client["app"].app_context():
        count = WishlistSubscriber.query.filter_by(email="alice@startup.com").count()
        assert count == 1


def test_subscribe_validation_errors(app_and_client):
    client = app_and_client["client"]
    # Empty body
    res_empty = client.post("/api/wishlist/subscribe", json={})
    assert res_empty.status_code == 400
    assert res_empty.get_json()["code"] == "EMAIL_REQUIRED"

    # Malformed email
    res_malformed = client.post("/api/wishlist/subscribe", json={"email": "not-an-email"})
    assert res_malformed.status_code == 400
    assert res_malformed.get_json()["code"] == "INVALID_EMAIL"


def test_admin_subscribers_endpoint_permissions(app_and_client):
    client = app_and_client["client"]
    user_token = app_and_client["user_token"]
    admin_token = app_and_client["admin_token"]

    # Pre-populate a subscriber
    client.post("/api/wishlist/subscribe", json={"email": "lead1@example.com"})

    # 1. Without auth
    res_no_auth = client.get("/api/wishlist/subscribers")
    assert res_no_auth.status_code == 401

    # 2. Regular user (forbidden)
    res_user = client.get("/api/wishlist/subscribers", headers={"Authorization": f"Bearer {user_token}"})
    assert res_user.status_code == 403

    # 3. Admin user (authorized)
    res_admin = client.get("/api/wishlist/subscribers", headers={"Authorization": f"Bearer {admin_token}"})
    assert res_admin.status_code == 200
    data = res_admin.get_json()
    assert data["success"] is True
    assert data["total"] >= 1
    assert any(s["email"] == "lead1@example.com" for s in data["subscribers"])


def test_admin_export_csv(app_and_client):
    client = app_and_client["client"]
    admin_token = app_and_client["admin_token"]

    # Pre-populate
    client.post("/api/wishlist/subscribe", json={"email": "export_lead@domain.com"})

    res = client.get("/api/wishlist/export", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 200
    assert res.mimetype == "text/csv"
    text = res.data.decode("utf-8")
    assert "Email Address" in text
    assert "export_lead@domain.com" in text
