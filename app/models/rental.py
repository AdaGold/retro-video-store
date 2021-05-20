from sqlalchemy.orm import relationship
from app import db
from datetime import datetime, timezone, timedelta


class Rental(db.Model):
    customer_id = db.Column("customer_id", db.Integer, db.ForeignKey(
        'customer.customer_id',  ondelete="CASCADE"), primary_key=True)
    video_id = db.Column("video_id", db.Integer, db.ForeignKey('video.video_id', ondelete="CASCADE"), primary_key=True)
    video = relationship("Video", back_populates="customers")
    customer = relationship("Customer", back_populates="videos")
    due_date = db.Column(db.Date(), default=datetime.now(timezone.utc) + timedelta(days=7))

    def as_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": self.customer.get_checked_count(),
            "available_inventory": self.video.get_inventory()
        }
