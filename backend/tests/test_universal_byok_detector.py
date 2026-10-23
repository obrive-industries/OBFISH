"""
Unit and integration tests for the Universal Zero-Config BYOK (Bring Your Own Key) system.
Tests detection across NVIDIA NIM, Alibaba Cloud DashScope, OpenRouter, Groq, Gemini, OpenAI,
DeepSeek, model resolution fallbacks, and live probe mocks.
"""

import pytest
from unittest.mock import patch, MagicMock
from app import create_app
from app.models.user import db, User
from app.config import Config
from app.utils.byok_detector import (
    detect_provider_from_key,
    resolve_model_for_base_url,
    probe_llm_key,
    PROVIDERS
)


@pytest.fixture
def app_instance(tmp_path):
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path}/test_byok.db"
        JWT_SECRET_KEY = "test-jwt-secret-key-byok"
        REQUIRE_BYOK = False

    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app, tmp_path
        db.session.remove()
        db.drop_all()


def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}


class TestProviderDetection:
    def test_nvidia_detection(self):
        detected = detect_provider_from_key("nvapi-test1234567890abcdef")
        assert detected["provider"] == "nvidia"
        assert detected["name"] == "NVIDIA NIM"
        assert detected["base_url"] == "https://integrate.api.nvidia.com/v1"
        assert detected["default_model"] == "meta/llama-3.1-8b-instruct"

    def test_openrouter_detection(self):
        detected = detect_provider_from_key("sk-or-v1-abcdef1234567890")
        assert detected["provider"] == "openrouter"
        assert detected["name"] == "OpenRouter"
        assert detected["base_url"] == "https://openrouter.ai/api/v1"
        assert detected["default_model"] == "openai/gpt-4o-mini"
        assert "HTTP-Referer" in detected["headers"]
        assert "X-Title" in detected["headers"]

    def test_alibaba_detection(self):
        detected = detect_provider_from_key("qwen-testkey-dashscope")
        assert detected["provider"] == "alibaba"
        assert detected["name"] == "Alibaba Cloud (DashScope)"
        assert detected["base_url"] == "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
        assert detected["default_model"] == "qwen-plus"

    def test_groq_detection(self):
        detected = detect_provider_from_key("gsk_test1234567890groq")
        assert detected["provider"] == "groq"
        assert detected["name"] == "Groq"
        assert detected["base_url"] == "https://api.groq.com/openai/v1"
        assert detected["default_model"] == "openai/gpt-oss-20b"

    def test_gemini_detection(self):
        detected = detect_provider_from_key("AIzaSyTestGeminiKey12345")
        assert detected["provider"] == "gemini"
        assert detected["name"] == "Google Gemini"
        assert detected["base_url"] == "https://generativelanguage.googleapis.com/v1beta/openai/"
        assert detected["default_model"] == "gemini-1.5-flash"

    def test_openai_detection(self):
        detected_proj = detect_provider_from_key("sk-proj-test123openai")
        assert detected_proj["provider"] == "openai"
        assert detected_proj["base_url"] == "https://api.openai.com/v1"
        assert detected_proj["default_model"] == "gpt-4o-mini"

        detected_sk = detect_provider_from_key("sk-test123openai")
        assert detected_sk["provider"] == "openai"

    def test_hint_overrides(self):
        detected = detect_provider_from_key("any-random-key", hint_provider="deepseek")
        assert detected["provider"] == "deepseek"
        assert detected["base_url"] == "https://api.deepseek.com/v1"
        assert detected["default_model"] == "deepseek-chat"

        detected_ali = detect_provider_from_key("random-key", hint_provider="alibaba")
        assert detected_ali["provider"] == "alibaba"
        assert detected_ali["default_model"] == "qwen-plus"

    def test_custom_fallback(self):
        detected = detect_provider_from_key("unknown-key-format-12345")
        assert detected["provider"] == "custom"


class TestModelResolution:
    def test_explicit_model_preserved(self):
        assert resolve_model_for_base_url("https://api.groq.com/openai/v1", "custom-model") == "custom-model"

    def test_nvidia_url_resolution(self):
        assert resolve_model_for_base_url("https://integrate.api.nvidia.com/v1", None) == "meta/llama-3.1-8b-instruct"

    def test_alibaba_url_resolution(self):
        assert resolve_model_for_base_url("https://dashscope-intl.aliyuncs.com/compatible-mode/v1", None) == "qwen-plus"

    def test_openrouter_url_resolution(self):
        assert resolve_model_for_base_url("https://openrouter.ai/api/v1", None) == "openai/gpt-4o-mini"

    def test_gemini_url_resolution(self):
        assert resolve_model_for_base_url("https://generativelanguage.googleapis.com/v1beta/openai/", None) == "gemini-1.5-flash"

    def test_groq_url_resolution(self):
        assert resolve_model_for_base_url("https://api.groq.com/openai/v1", None) == "openai/gpt-oss-20b"


class TestKeyProbing:
    def test_empty_key(self):
        res = probe_llm_key("")
        assert res["success"] is False
        assert "empty" in res["error"].lower()

    @patch("requests.post")
    @patch("requests.get")
    def test_probe_success(self, mock_get, mock_post):
        mock_get_resp = MagicMock()
        mock_get_resp.status_code = 200
        mock_get_resp.json.return_value = {
            "data": [{"id": "meta/llama-3.1-8b-instruct"}, {"id": "meta/llama-3.3-70b-instruct"}]
        }
        mock_get.return_value = mock_get_resp

        mock_post_resp = MagicMock()
        mock_post_resp.status_code = 200
        mock_post_resp.json.return_value = {"choices": [{"message": {"content": "Hello"}}]}
        mock_post.return_value = mock_post_resp

        result = probe_llm_key("nvapi-mockkey123")
        assert result["success"] is True
        assert result["provider"] == "nvidia"
        assert result["model"] == "meta/llama-3.1-8b-instruct"
        assert "Verified successfully" in result["message"]

    @patch("requests.post")
    @patch("requests.get")
    def test_probe_failure_response(self, mock_get, mock_post):
        mock_get.side_effect = Exception("Network unreachable")

        mock_post_resp = MagicMock()
        mock_post_resp.status_code = 401
        mock_post_resp.text = "Unauthorized: Invalid API key"
        mock_post.return_value = mock_post_resp

        result = probe_llm_key("sk-invalidkey")
        assert result["success"] is False
        assert "401" in result["error"]


class TestAuthBYOKIntegration:
    def test_probe_endpoint_and_profile_autodetect(self, app_instance):
        app, tmp_path = app_instance
        client = app.test_client()

        # 1. Register & verify user
        user = User(full_name="byokuser", email="byok@obrive.com", is_verified=True)
        user.set_password("SecurePass123!")
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            user_id = user.id

        login_res = client.post("/api/auth/login", json={
            "email": "byok@obrive.com",
            "password": "SecurePass123!"
        })
        assert login_res.status_code == 200
        token = login_res.json["access_token"]

        # 2. Test /api/auth/probe-llm-key endpoint
        with patch("app.utils.byok_detector.probe_llm_key") as mock_probe:
            mock_probe.return_value = {
                "success": True,
                "provider": "openrouter",
                "provider_name": "OpenRouter",
                "base_url": "https://openrouter.ai/api/v1",
                "model": "openai/gpt-4o-mini",
                "message": "Verified successfully with OpenRouter!"
            }
            probe_res = client.post(
                "/api/auth/probe-llm-key",
                headers=_auth_header(token),
                json={"api_key": "sk-or-v1-samplekey"}
            )
            assert probe_res.status_code == 200
            assert probe_res.json["success"] is True
            assert probe_res.json["provider"] == "openrouter"

        # 3. Test profile auto-detection on save
        # User provides ONLY custom_llm_api_key="nvapi-demo" without base_url or model
        update_res = client.put(
            "/api/auth/profile",
            headers=_auth_header(token),
            json={"custom_llm_api_key": "nvapi-demokey12345"}
        )
        assert update_res.status_code == 200
        data = update_res.json["user"]
        assert data["has_custom_api_key"] is True
        assert data["custom_llm_base_url"] == "https://integrate.api.nvidia.com/v1"
        assert data["custom_llm_model_name"] == "meta/llama-3.1-8b-instruct"

        # Verify DB directly
        with app.app_context():
            u = db.session.get(User, user_id)
            assert u.custom_llm_base_url == "https://integrate.api.nvidia.com/v1"
            assert u.custom_llm_model_name == "meta/llama-3.1-8b-instruct"
            assert u.custom_llm_api_key.startswith("nvapi-")
