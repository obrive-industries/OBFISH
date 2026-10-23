"""
Brain Email Service
Sends transactional emails (verification, password reset) via SMTP.
Reads config from environment variables — no credentials in code.

Required env vars:
  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
  SMTP_FROM_NAME, SMTP_FROM_EMAIL
  APP_BASE_URL  (e.g. https://brain.obrive.com)
"""

import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

logger = logging.getLogger("brain.email")


def _get_smtp_config():
    """Retrieve latest SMTP settings from environment on demand."""
    host = os.environ.get("SMTP_HOST", "smtp-relay.brevo.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER", "")
    password = os.environ.get("SMTP_PASSWORD", "")
    from_name = os.environ.get("SMTP_FROM_NAME", "Brain")
    from_email = os.environ.get("SMTP_FROM_EMAIL", "ai@obrive.com") or user
    app_base_url = os.environ.get("APP_BASE_URL", "https://brain.obrive.com").rstrip("/")
    return host, port, user, password, from_name, from_email, app_base_url


# ------------------------------------------------------------------ #
# Internal send helper
# ------------------------------------------------------------------ #

def _send(to_email: str, subject: str, html_body: str, text_body: str) -> bool:
    """
    Send a multipart email (HTML + plain-text fallback) via SMTP TLS.
    Returns True on success, False on failure (error is logged, never raised).
    """
    host, port, user, password, from_name, from_email, _ = _get_smtp_config()

    if not user or not password:
        # Dev mode: just log the email content instead of sending
        logger.warning(
            "[DEV MODE] SMTP not configured — email NOT sent.\n"
            f"  To: {to_email}\n  Subject: {subject}\n  Body:\n{text_body}"
        )
        return True

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(host, port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user, password)
            server.sendmail(from_email, [to_email], msg.as_string())
        logger.info(f"Email sent successfully: {subject!r} → {to_email}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send email to {to_email}: {exc}", exc_info=True)
        return False


# ------------------------------------------------------------------ #
# Email templates
# ------------------------------------------------------------------ #

def _base_html(title: str, content: str) -> str:
    """Minimal, inline-styled HTML wrapper matching Brain brand."""
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
                BRAIN
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
                This email was sent by Brain · Obrive Technologies<br/>
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

def send_verification_email(to_email: str, full_name: str, otp: str) -> bool:
    """
    Send a 6-digit OTP verification code to the user's email.
    """
    content = f"""
      <h2 style="margin:0 0 8px;font-size:24px;color:#074139;">Welcome to Brain!</h2>
      <p style="margin:0 0 20px;color:#526361;font-size:14px;line-height:1.6;">
        Hi <strong>{full_name}</strong>,<br/>
        Please use the 6-digit verification code below to activate your account and start your simulation engines:
      </p>

      <div style="margin:24px 0 28px;text-align:center;">
        <div style="display:inline-block;background:#EBF7F4;border:2px dashed #074139;border-radius:12px;padding:16px 36px;">
          <span style="font-family:'Courier New', monospace, sans-serif;font-size:36px;font-weight:800;letter-spacing:10px;color:#074139;">
            {otp}
          </span>
        </div>
      </div>

      <p style="margin:0 0 8px;font-size:13px;color:#526361;text-align:center;">
        Enter this code in Brain to complete verification.
      </p>

      <p style="margin:24px 0 0;font-size:12px;color:#9CA3AF;text-align:center;">
        This code expires in <strong>15 minutes</strong>. If you did not request this, you can safely ignore this email.
      </p>
    """

    text_body = (
        f"Hi {full_name},\n\n"
        f"Your Brain verification code is: {otp}\n\n"
        "Enter this 6-digit code in Brain to activate your account.\n"
        "This code expires in 15 minutes.\n\n"
        "— Brain by Obrive"
    )

    return _send(
        to_email=to_email,
        subject=f"{otp} is your Brain verification code",
        html_body=_base_html("Verify your email", content),
        text_body=text_body,
    )


def send_password_reset_email(to_email: str, full_name: str, token: str) -> bool:
    """
    Send a password reset link. Token expires in 30 minutes.
    """
    _, _, _, _, _, _, app_base_url = _get_smtp_config()
    reset_url = f"{app_base_url}/reset-password?token={token}"

    content = f"""
      <h2 style="margin:0 0 8px;font-size:24px;color:#074139;">Reset your password</h2>
      <p style="margin:0 0 20px;color:#526361;font-size:14px;line-height:1.6;">
        Hi <strong>{full_name}</strong>,<br/>
        We received a request to reset your Brain password.
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
        "Reset your Brain password using the link below:\n\n"
        f"{reset_url}\n\n"
        "This link expires in 30 minutes.\n"
        "If you did not request this, you can safely ignore this email.\n\n"
        "— Brain by Obrive"
    )

    return _send(
        to_email=to_email,
        subject="Reset your Brain password",
        html_body=_base_html("Reset your password", content),
        text_body=text_body,
    )


def send_welcome_email(to_email: str, full_name: str) -> bool:
    """
    Send a welcome email after account is successfully verified.
    """
    _, _, _, _, _, _, app_base_url = _get_smtp_config()
    content = f"""
      <h2 style="margin:0 0 8px;font-size:24px;color:#074139;">You're in! 🎉</h2>
      <p style="margin:0 0 20px;color:#526361;font-size:14px;line-height:1.6;">
        Hi <strong>{full_name}</strong>,<br/>
        Your Brain account is now verified and ready to use.
        Upload a seed dossier and let our swarm intelligence engine predict the future for you.
      </p>
      <p style="margin:0 0 28px;">
        <a href="{app_base_url}/"
           style="display:inline-block;background:#074139;color:#A2F1DF;text-decoration:none;
                  padding:14px 32px;border-radius:8px;font-weight:700;font-size:15px;">
          Launch Brain →
        </a>
      </p>
    """

    text_body = (
        f"Hi {full_name},\n\nYour Brain account is verified!\n\n"
        f"Launch the platform: {app_base_url}/\n\n— Brain by Obrive"
    )

    return _send(
        to_email=to_email,
        subject="Welcome to Brain — Your account is ready!",
        html_body=_base_html("Welcome to Brain", content),
        text_body=text_body,
    )
