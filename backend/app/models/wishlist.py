"""
Wishlist Subscriber Model
Stores emails captured from the landing page wishlist/waitlist form.
"""

from datetime import datetime, timezone
from .user import db


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class WishlistSubscriber(db.Model):
    """Stores wishlist/waitlist leads captured from the marketing landing page."""

    __tablename__ = "wishlist_subscribers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    source = db.Column(db.String(100), nullable=False, default="landing_hero")
    status = db.Column(db.String(50), nullable=False, default="active")
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=_utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "source": self.source,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
