"""
ObMind Email Service
Sends transactional emails (verification, password reset) via SMTP.
Reads config from environment variables — no credentials in code.

Required env vars:
  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
  SMTP_FROM_NAME, SMTP_FROM_EMAIL
  APP_BASE_URL  (e.g. https://obfish.obrive.com)
"""

import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

logger = logging.getLogger("obmind.email")


# ------------------------------------------------------------------ #
# Config (read once at import time)
# ------------------------------------------------------------------ #
_SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
_SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
_SMTP_USER = os.environ.get("SMTP_USER", "")
_SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
_FROM_NAME = os.environ.get("SMTP_FROM_NAME", "ObMind by Obrive")
_FROM_EMAIL = os.environ.get("SMTP_FROM_EMAIL", _SMTP_USER)
_APP_BASE_URL = os.environ.get("APP_BASE_URL", "https://obfish.obrive.com").rstrip("/")


# ------------------------------------------------------------------ #
# Internal send helper
# ------------------------------------------------------------------ #

def _send(to_email: str, subject: str, html_body: str, text_body: str) -> bool:
    """
    Send a multipart email (HTML + plain-text fallback) via SMTP TLS.
    Returns True on success, False on failure (error is logged, never raised).
    """
    if not _SMTP_USER or not _SMTP_PASSWORD:
        # Dev mode: just log the email content instead of sending
        logger.warning(
            "[DEV MODE] SMTP not configured — email NOT sent.\n"
            f"  To: {to_email}\n  Subject: {subject}\n  Body:\n{text_body}"
        )
        return True

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{_FROM_NAME} <{_FROM_EMAIL}>"
    msg["To"] = to_email

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.login(_SMTP_USER, _SMTP_PASSWORD)
            server.sendmail(_FROM_EMAIL, [to_email], msg.as_string())
        logger.info(f"Email sent: {subject!r} → {to_email}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send email to {to_email}: {exc}", exc_info=True)
        return False


# ------------------------------------------------------------------ #
# Email templates
# ------------------------------------------------------------------ #

def _base_html(title: str, content: str) -> str:
    """Minimal, inline-styled HTML wrapper matching ObMind brand."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
</head>
<body style="margin:0;padding:0;background:#A2F1DF;font-family:'Segoe UI',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#A2F1DF;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="560" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(7,65,57,0.12);">

          <!-- Header -->
          <tr>
            <td style="background:#074139;padding:28px 40px;">
              <p style="margin:0;font-size:22px;font-weight:700;color:#A2F1DF;letter-spacing:3px;">
                OBMIND
              </p>
              <p style="margin:4px 0 0;font-size:11px;color:rgba(162,241,223,0.7);letter-spacing:1px;text-transform:uppercase;">
                by Obrive
              </p>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:36px 40px;color:#074139;">
              {content}
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:20px 40px;border-top:1px solid #E0F7F2;background:#F8FDFC;">
              <p style="margin:0;font-size:12px;color:#526361;line-height:1.6;">
                This email was sent by ObMind · Obrive Technologies<br/>
                If you didn't request this, you can safely ignore this email.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


# ------------------------------------------------------------------ #
# Public API
# ------------------------------------------------------------------ #

def send_verification_email(to_email: str, full_name: str, token: str) -> bool:
    """
    Send an email address verification link to the user.
    The link points to: /verify-email?token=<token>
    """
    verify_url = f"{_APP_BASE_URL}/verify-email?token={token}"

    content = f"""
      <h2 style="margin:0 0 8px;font-size:24px;color:#074139;">Welcome to ObMind!</h2>
      <p style="margin:0 0 20px;color:#526361;font-size:14px;line-height:1.6;">
        Hi <strong>{full_name}</strong>,<br/>
        Thank you for signing up. Please verify your email address to activate your account.
      </p>

      <p style="margin:0 0 28px;">
        <a href="{verify_url}"
           style="display:inline-block;background:#074139;color:#A2F1DF;text-decoration:none;
                  padding:14px 32px;border-radius:8px;font-weight:700;font-size:15px;
                  letter-spacing:0.5px;">
          Verify My Email →
        </a>
      </p>

      <p style="margin:0 0 8px;font-size:13px;color:#526361;">
        Or copy this link into your browser:
      </p>
      <p style="margin:0;font-size:12px;word-break:break-all;color:#074139;
                background:#E0F7F2;padding:10px 14px;border-radius:6px;font-family:monospace;">
        {verify_url}
      </p>

      <p style="margin:24px 0 0;font-size:12px;color:#9CA3AF;">
        This link expires in <strong>24 hours</strong>.
      </p>
    """

    text_body = (
        f"Hi {full_name},\n\n"
        "Please verify your ObMind email address by visiting the link below:\n\n"
        f"{verify_url}\n\n"
        "This link expires in 24 hours.\n\n"
        "— ObMind by Obrive"
    )

    return _send(
        to_email=to_email,
        subject="Verify your ObMind email address",
        html_body=_base_html("Verify your email", content),
        text_body=text_body,
    )


def send_password_reset_email(to_email: str, full_name: str, token: str) -> bool:
    """
    Send a password reset link. Token expires in 30 minutes.
    """
    reset_url = f"{_APP_BASE_URL}/reset-password?token={token}"

    content = f"""
      <h2 style="margin:0 0 8px;font-size:24px;color:#074139;">Reset your password</h2>
      <p style="margin:0 0 20px;color:#526361;font-size:14px;line-height:1.6;">
        Hi <strong>{full_name}</strong>,<br/>
        We received a request to reset your ObMind password.
        Click the button below to choose a new one.
      </p>

      <p style="margin:0 0 28px;">
        <a href="{reset_url}"
           style="display:inline-block;background:#074139;color:#A2F1DF;text-decoration:none;
                  padding:14px 32px;border-radius:8px;font-weight:700;font-size:15px;
                  letter-spacing:0.5px;">
          Reset Password →
        </a>
      </p>

      <p style="margin:0 0 8px;font-size:13px;color:#526361;">
        Or copy this link:
      </p>
      <p style="margin:0;font-size:12px;word-break:break-all;color:#074139;
                background:#E0F7F2;padding:10px 14px;border-radius:6px;font-family:monospace;">
        {reset_url}
      </p>

      <p style="margin:24px 0 0;font-size:12px;color:#e53e3e;">
        ⚠️ This link expires in <strong>30 minutes</strong>.
        If you did not request a password reset, please ignore this email.
      </p>
    """

    text_body = (
        f"Hi {full_name},\n\n"
        "Reset your ObMind password using the link below:\n\n"
        f"{reset_url}\n\n"
        "This link expires in 30 minutes.\n"
        "If you did not request this, you can safely ignore this email.\n\n"
        "— ObMind by Obrive"
    )

    return _send(
        to_email=to_email,
        subject="Reset your ObMind password",
        html_body=_base_html("Reset your password", content),
        text_body=text_body,
    )


def send_welcome_email(to_email: str, full_name: str) -> bool:
    """
    Send a welcome email after account is successfully verified.
    """
    content = f"""
      <h2 style="margin:0 0 8px;font-size:24px;color:#074139;">You're in! 🎉</h2>
      <p style="margin:0 0 20px;color:#526361;font-size:14px;line-height:1.6;">
        Hi <strong>{full_name}</strong>,<br/>
        Your ObMind account is now verified and ready to use.
        Upload a seed dossier and let our swarm intelligence engine predict the future for you.
      </p>
      <p style="margin:0 0 28px;">
        <a href="{_APP_BASE_URL}/"
           style="display:inline-block;background:#074139;color:#A2F1DF;text-decoration:none;
                  padding:14px 32px;border-radius:8px;font-weight:700;font-size:15px;">
          Launch ObMind →
        </a>
      </p>
    """

    text_body = (
        f"Hi {full_name},\n\nYour ObMind account is verified!\n\n"
        f"Launch the platform: {_APP_BASE_URL}/\n\n— ObMind by Obrive"
    )

    return _send(
        to_email=to_email,
        subject="Welcome to ObMind — Your account is ready!",
        html_body=_base_html("Welcome to ObMind", content),
        text_body=text_body,
    )
