from datetime import datetime, timedelta
from flask import current_app
from sqlalchemy.orm import backref, relation, relationship
from app import db
from sqlalchemy import DateTime
from .customer import Customer
from .video import Video

class Rental(db.Model):
    __tablename__ = 'rentals'
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'), nullable=True)
    due_date = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(days=7))

    # backref for customer & video only needed if back_populate is being used
    # customer = db.relationship('Customer', backref='customer', lazy=True)
    # video = db.relationship('Video', backref='video', lazy=True)

    def to_json(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
        }