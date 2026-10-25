#!/usr/bin/env python3
"""
Brain - Admin Sync & Reset CLI Tool
Usage:
    python backend/scripts/reset_admin.py [optional_email] [optional_password]
"""

import os
import sys

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models.user import User
from app.config import Config


def main():
    app = create_app()
    with app.app_context():
        # Read args or defaults
        custom_email = sys.argv[1].strip().lower() if len(sys.argv) > 1 else None
        custom_pass = sys.argv[2].strip() if len(sys.argv) > 2 else os.environ.get("ADMIN_PASSWORD", "Yashveer@2910")

        admin_emails = list(Config.admin_emails())
        if custom_email and custom_email not in admin_emails:
            admin_emails.append(custom_email)

        print("=" * 60)
        print(" Brain - Administrator Account Synchronization")
        print("=" * 60)
        print(f"Target Admin Accounts: {', '.join(admin_emails)}")
        print("-" * 60)

        for email in admin_emails:
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(
                    email=email,
                    full_name="Obrive Admin",
                    is_verified=True,
                    role="admin"
                )
                user.set_password(custom_pass)
                db.session.add(user)
                print(f"[+] Created fresh admin: {email}")
            else:
                user.role = "admin"
                user.is_verified = True
                user.is_active = True
                user.set_password(custom_pass)
                print(f"[+] Updated existing admin: {email} (role=admin, verified=True)")

        db.session.commit()
        print("=" * 60)
        print("✅ SUCCESS: Admin accounts are fully synchronized and active!")
        print("   Sign in at: https://brain.obrive.com/console (or http://localhost:3000/console)")
        print(f"   Admin Emails: {', '.join(admin_emails)}")
        print("=" * 60)


if __name__ == "__main__":
    main()
