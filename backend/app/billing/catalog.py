"""Single source of truth for subscription plans, prices and limits."""

from __future__ import annotations

from typing import Any

from ..config import Config

CURRENCY = "USD"

# Razorpay Plan IDs are provisioned once by backend/scripts/setup_razorpay_plans.py
# and supplied through the environment.
RAZORPAY_PLAN_ID_ENV = {
    ("starter", "monthly"): "RAZORPAY_PLAN_ID_STARTER_MONTHLY",
    ("starter", "annual"): "RAZORPAY_PLAN_ID_STARTER_ANNUAL",
    ("pro", "monthly"): "RAZORPAY_PLAN_ID_PRO_MONTHLY",
    ("pro", "annual"): "RAZORPAY_PLAN_ID_PRO_ANNUAL",
    ("premium", "monthly"): "RAZORPAY_PLAN_ID_PREMIUM_MONTHLY",
    ("premium", "annual"): "RAZORPAY_PLAN_ID_PREMIUM_ANNUAL",
}

PLAN_CATALOG: list[dict[str, Any]] = [
    {
        "id": "starter",
        "name": "Starter",
        "badge": None,
        "monthly_cents": 1000,
        "annual_cents": 6000,
        "monthly_equivalent_cents": 500,
        "annual_strike_cents": 1000,
        "inr_monthly_paise": 85000,
        "inr_annual_paise": 510000,
        "description": {
            "monthly": (
                "For first paid runs when you want to take one real case "
                "from source material to prediction report."
            ),
            "annual": (
                "For first paid runs when you already know you want a lower "
                "annual cost for recurring work."
            ),
        },
        "features": {
            "monthly": [
                "Upload PDF, Markdown, and text seed material",
                "Turn source material into ontology and graph structure",
                "Run parallel simulation and generate a prediction report",
                "Continue analysis with follow-up questions in the same workspace",
                "Email support",
            ],
            "annual": [
                "Upload PDF, Markdown, and text seed material",
                "Turn source material into ontology and graph structure",
                "Run parallel simulation and generate a prediction report",
                "Continue analysis with follow-up questions in the same workspace",
                "Email support",
            ],
        },
        "footnote": {
            "monthly": (
                "Start here if you want to validate one active prediction "
                "workflow before committing further."
            ),
            "annual": (
                "Best entry point if you already expect to run Brain "
                "through the year."
            ),
        },
        "cta": "Choose Starter",
        "limits": {
            "runs_per_period": {"monthly": 3, "annual": 36},
            "max_rounds": 15,
        },
    },
    {
        "id": "pro",
        "name": "Pro",
        "badge": "MOST POPULAR",
        "monthly_cents": 2000,
        "annual_cents": 18000,
        "monthly_equivalent_cents": 1500,
        "annual_strike_cents": 2500,
        "inr_monthly_paise": 170000,
        "inr_annual_paise": 1530000,
        "description": {
            "monthly": (
                "For recurring simulation work across public-opinion, "
                "market, and narrative scenarios."
            ),
            "annual": (
                "For recurring simulation work across public-opinion, "
                "market, and narrative scenarios."
            ),
        },
        "features": {
            "monthly": [
                "Everything in Starter",
                "More monthly simulation capacity",
                "Better for repeated scenario review and comparison",
                "Built for ongoing report, risk, and narrative analysis",
                "Priority email support",
            ],
            "annual": [
                "Everything in Starter",
                "More yearly simulation capacity at a lower annual cost",
                "Better for repeated scenario review and comparison",
                "Built for ongoing report, risk, and narrative analysis",
                "Priority email support",
            ],
        },
        "footnote": {
            "monthly": (
                "Choose Pro when Brain becomes part of your normal weekly "
                "research loop."
            ),
            "annual": (
                "Best value once Brain is part of your normal weekly "
                "operating rhythm."
            ),
        },
        "cta": "Choose Pro",
        "limits": {
            "runs_per_period": {"monthly": 10, "annual": 120},
            "max_rounds": 40,
        },
    },
    {
        "id": "premium",
        "name": "Premium",
        "badge": "HIGHEST CAPACITY",
        "monthly_cents": 3000,
        "annual_cents": 30000,
        "monthly_equivalent_cents": 2500,
        "annual_strike_cents": 3500,
        "inr_monthly_paise": 255000,
        "inr_annual_paise": 2550000,
        "description": {
            "monthly": (
                "For heavy, continuous simulation usage when you are "
                "iterating on live questions and refreshing reports often."
            ),
            "annual": (
                "For heavy, continuous simulation usage when you are "
                "iterating on live questions and refreshing reports often."
            ),
        },
        "features": {
            "monthly": [
                "Everything in Pro",
                "Highest monthly simulation capacity",
                "Best for heavier iteration across multiple live questions",
                "More headroom for continuous simulation and report refreshes",
                "Priority support",
            ],
            "annual": [
                "Everything in Pro",
                "Highest yearly simulation capacity",
                "Best for heavier iteration across multiple live questions",
                "More headroom for continuous simulation and report refreshes",
                "Priority support",
            ],
        },
        "footnote": {
            "monthly": (
                "Choose Premium when throughput matters more than keeping "
                "the lowest monthly spend."
            ),
            "annual": (
                "Choose Premium when Brain stays in your operating loop all "
                "year and throughput matters most."
            ),
        },
        "cta": "Choose Premium",
        "limits": {
            "runs_per_period": {"monthly": 30, "annual": 360},
            "max_rounds": 80,
        },
    },
]

PLAN_BY_ID = {plan["id"]: plan for plan in PLAN_CATALOG}


def get_plan(plan_id: str | None) -> dict[str, Any] | None:
    """Return a plan definition by id, or None for unknown/free plans."""

    return PLAN_BY_ID.get((plan_id or "").strip().lower())


def get_razorpay_plan_id(plan_id: str, interval: str) -> str | None:
    """Return the configured Razorpay plan id for a tier and billing interval."""

    env_name = RAZORPAY_PLAN_ID_ENV.get((plan_id, interval))
    if not env_name:
        return None
    value = getattr(Config, env_name, None)
    return value.strip() if isinstance(value, str) and value.strip() else None


def plan_from_razorpay_id(razorpay_plan_id: str | None) -> tuple[str, str] | None:
    """Map a Razorpay plan id back to (tier, interval) using the env config."""

    if not razorpay_plan_id:
        return None
    for key, env_name in RAZORPAY_PLAN_ID_ENV.items():
        configured = getattr(Config, env_name, None)
        if configured and configured.strip() == str(razorpay_plan_id).strip():
            return key
    return None


def billing_configured() -> bool:
    """True when checkout can be created for every tier and interval."""

    if not Config.RAZORPAY_KEY_ID or not Config.RAZORPAY_KEY_SECRET:
        return False
    return all(
        get_razorpay_plan_id(plan_id, interval)
        for plan_id, interval in RAZORPAY_PLAN_ID_ENV
    )


def public_catalog() -> dict[str, Any]:
    """Plan data safe to expose to the browser."""

    plans = []
    for plan in PLAN_CATALOG:
        plans.append(
            {
                "id": plan["id"],
                "name": plan["name"],
                "badge": plan["badge"],
                "monthly_cents": plan["monthly_cents"],
                "annual_cents": plan["annual_cents"],
                "monthly_equivalent_cents": plan["monthly_equivalent_cents"],
                "annual_strike_cents": plan.get("annual_strike_cents", plan["monthly_cents"]),
                "description": plan["description"],
                "features": plan["features"],
                "footnote": plan["footnote"],
                "cta": plan["cta"],
                "limits": plan["limits"],
            }
        )
    return {
        "currency": CURRENCY,
        "annual_discount_percent": 50,
        "plans": plans,
        "configured": billing_configured(),
    }
