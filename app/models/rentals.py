from flask import current_app
from app import db
from flask_sqlalchemy import SQLAlchemy

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), primary_key=True)
    due_date = db.Column(db.DateTime)
    customer = db.relationship("Customer", back_populates="videos")
    video = db.relationship("Video", back_populates="customers")
    __tablename__ = "rentals"

    def to_json(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
            }