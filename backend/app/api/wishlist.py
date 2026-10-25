"""
Brain Wishlist API — /api/wishlist/*
Endpoints:
  POST /api/wishlist/subscribe   Capture new wishlist email (Public)
  GET  /api/wishlist/subscribers View all collected emails (Admin only)
  GET  /api/wishlist/export      Export subscribers as CSV (Admin only)
"""

import io
import csv
import re
import logging
from flask import Blueprint, request, jsonify, Response

from ..models.user import db
from ..models.wishlist import WishlistSubscriber
from ..utils.auth_middleware import require_auth, get_current_user

logger = logging.getLogger("brain.wishlist")

wishlist_bp = Blueprint("wishlist", __name__)

EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[\w\-]+(\.[a-zA-Z0-9\-]+)+$")


@wishlist_bp.route("/subscribe", methods=["POST"])
def subscribe():
    """
    Public endpoint to join the wishlist.
    Accepts JSON: { "email": "user@example.com", "source": "landing_hero" }
    """
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    source = data.get("source", "landing_hero").strip()

    if not email:
        return jsonify({
            "success": False,
            "error": "Email address is required.",
            "code": "EMAIL_REQUIRED"
        }), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({
            "success": False,
            "error": "Please provide a valid email address.",
            "code": "INVALID_EMAIL"
        }), 400

    try:
        existing = WishlistSubscriber.query.filter_by(email=email).first()
        if existing:
            return jsonify({
                "success": True,
                "already_subscribed": True,
                "message": "You're already on our wishlist! We'll notify you as soon as offers drop."
            }), 200

        subscriber = WishlistSubscriber(
            email=email,
            source=source or "landing_hero",
            status="active"
        )
        db.session.add(subscriber)
        db.session.commit()

        logger.info(f"New wishlist subscriber captured: {email}")
        return jsonify({
            "success": True,
            "already_subscribed": False,
            "message": "Thank you for joining our wishlist! We'll notify you about exclusive offers."
        }), 201

    except Exception as exc:
        db.session.rollback()
        logger.error(f"Failed to save wishlist subscriber {email}: {exc}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "Unable to save your request right now. Please try again.",
            "code": "SERVER_ERROR"
        }), 500


@wishlist_bp.route("/subscribers", methods=["GET"])
@require_auth
def get_subscribers():
    """
    Admin-only endpoint to list all wishlist subscribers.
    """
    current_user = get_current_user()
    if not current_user or current_user.role != "admin":
        return jsonify({
            "success": False,
            "error": "Administrator privileges required to access wishlist leads.",
            "code": "FORBIDDEN"
        }), 403

    try:
        subscribers = WishlistSubscriber.query.order_by(WishlistSubscriber.created_at.desc()).all()
        return jsonify({
            "success": True,
            "total": len(subscribers),
            "subscribers": [s.to_dict() for s in subscribers]
        }), 200
    except Exception as exc:
        logger.error(f"Error querying wishlist subscribers: {exc}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "Failed to retrieve wishlist subscribers.",
            "code": "DATABASE_ERROR"
        }), 500


@wishlist_bp.route("/export", methods=["GET"])
@require_auth
def export_csv():
    """
    Admin-only endpoint to download all wishlist subscribers as a CSV.
    """
    current_user = get_current_user()
    if not current_user or current_user.role != "admin":
        return jsonify({
            "success": False,
            "error": "Administrator privileges required.",
            "code": "FORBIDDEN"
        }), 403

    try:
        subscribers = WishlistSubscriber.query.order_by(WishlistSubscriber.created_at.desc()).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Email Address", "Source", "Status", "Subscribed At (UTC)"])

        for sub in subscribers:
            writer.writerow([
                sub.id,
                sub.email,
                sub.source,
                sub.status,
                sub.created_at.isoformat() if sub.created_at else ""
            ])

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=wishlist_subscribers.csv"}
        )
    except Exception as exc:
        logger.error(f"Error exporting wishlist subscribers: {exc}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "Failed to generate CSV export.",
            "code": "EXPORT_ERROR"
        }), 500
