from app import db
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime(), default = datetime.now(timezone.utc) + timedelta(days=7))
    customer = relationship("Customer", back_populates="videos")
    video = relationship("Video", back_populates="customers")
    
    def to_json(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
        }