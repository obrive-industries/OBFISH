#!/usr/bin/env python3
"""
CLI utility to create or reset the administrator account in the active database.

Usage:
    python backend/scripts/create_or_reset_admin.py [email] [password] [full_name]

Example:
    python backend/scripts/create_or_reset_admin.py ai@obrive.com Yashveer@2910 "Obrive Admin"
"""

import sys
import os

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models.user import db, User

def main():
    email = sys.argv[1] if len(sys.argv) > 1 else "ai@obrive.com"
    password = sys.argv[2] if len(sys.argv) > 2 else "Yashveer@2910"
    full_name = sys.argv[3] if len(sys.argv) > 3 else "Obrive Admin"

    print(f"Setting up administrator account: {email}")

    app = create_app()
    with app.app_context():
        db.create_all()
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(password)
            user.is_verified = True
            user.role = "admin"
            user.full_name = full_name
            user.token_version = getattr(user, 'token_version', 1) + 1
            db.session.commit()
            print(f"✅ Existing user '{email}' successfully updated:")
        else:
            user = User(
                email=email,
                full_name=full_name,
                is_verified=True,
                role="admin"
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"✅ New administrator user '{email}' successfully created:")

        print(f"   - Email: {user.email}")
        print(f"   - Role: {user.role}")
        print(f"   - Verified: {user.is_verified}")
        print(f"   - Password: [UPDATED TO '{password}']")
        print("\nYou can now sign in at https://brain.obrive.com with these credentials!")

if __name__ == "__main__":
    main()
