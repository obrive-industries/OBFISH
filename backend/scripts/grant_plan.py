"""Grant a plan to an account without a payment (QA, comps, support).

    cd backend
    uv run python scripts/grant_plan.py user@example.com pro monthly --days 30
"""

from __future__ import annotations

import argparse
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.billing.catalog import PLAN_BY_ID
from app.models.billing import Subscription, db
from app.models.user import User

app = create_app()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email")
    parser.add_argument("plan", choices=sorted(PLAN_BY_ID))
    parser.add_argument("interval", choices=["monthly", "annual"], nargs="?", default="monthly")
    parser.add_argument("--days", type=int, default=0, help="Override the period length")
    args = parser.parse_args()

    with app.app_context():
        user = User.query.filter_by(email=args.email.strip().lower()).first()
        if not user:
            print(f"No account found for {args.email}", file=sys.stderr)
            return 1

        now = datetime.now(timezone.utc)
        days = args.days or (366 if args.interval == "annual" else 31)
        period_end = now + timedelta(days=days)

        subscription = Subscription(
            user_id=user.id,
            provider="manual",
            provider_subscription_id=f"manual_{uuid.uuid4().hex}",
            plan=args.plan,
            billing_interval=args.interval,
            status="active",
            current_period_start=now,
            current_period_end=period_end,
        )
        db.session.add(subscription)
        db.session.commit()
        print(
            f"{user.email}: {args.plan}/{args.interval} active until "
            f"{period_end.isoformat()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
