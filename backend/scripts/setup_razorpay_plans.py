"""Create the Brain USD subscription plans in Razorpay.

Run once per Razorpay environment (test and live):

    cd backend
    uv run python scripts/setup_razorpay_plans.py

Then copy the printed RAZORPAY_PLAN_ID_* values into `.env`.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import razorpay

from app.billing.catalog import PLAN_CATALOG, get_razorpay_plan_id
from app.config import Config


def main() -> int:
    if not Config.RAZORPAY_KEY_ID or not Config.RAZORPAY_KEY_SECRET:
        print("Set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET first.", file=sys.stderr)
        return 1

    client = razorpay.Client(
        auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET)
    )
    env_lines: list[str] = []

    for plan in PLAN_CATALOG:
        for interval in ("monthly", "annual"):
            env_name = f"RAZORPAY_PLAN_ID_{plan['id'].upper()}_{interval.upper()}"
            if get_razorpay_plan_id(plan["id"], interval):
                print(f"{env_name}: already configured, skipping")
                continue
            amount = plan[f"{interval}_cents"]
            entity = client.plan.create(
                {
                    "period": "yearly" if interval == "annual" else "monthly",
                    "interval": 1,
                    "item": {
                        "name": f"Brain {plan['name']} ({interval})",
                        "amount": amount,
                        "currency": "USD",
                        "description": plan["description"][interval][:250],
                    },
                }
            )
            plan_id = entity.get("id")
            if not plan_id:
                print(f"Razorpay returned no plan id for {env_name}", file=sys.stderr)
                return 1
            env_lines.append(f"{env_name}={plan_id}")
            print(f"created {env_name} -> {plan_id}")

    if env_lines:
        print("\nAdd these to .env (and to the production environment):")
        print("\n".join(env_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
