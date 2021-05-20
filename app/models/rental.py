from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(days=7))
    customer = db.relationship("Customer", back_populates="rentals", lazy=True)
    video = db.relationship("Video", back_populates="rentals", lazy=True)

    def rental_to_json(self):
        to_json = {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
            }
        return to_json