from flask import current_app
from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from app.models.video import Video
from app.models.customer import Customer

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    checkout_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    check_in_date = db.Column(db.DateTime, nullable=True, default=None)
    # customer = db.relationship("Customer", back_populates="videos")
    # video = db.relationship("Video", back_populates="customers")
    __tablename__ = "rentals"

    def check_rental_to_json(self):
        customer = Customer.query.get(self.customer_id)
        video = Video.query.get(self.video_id)
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "check_in_date": self.check_in_date,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.available_inventory,
            }
    
    def overdue_to_json(self):
        customer = Customer.query.get(self.customer_id)
        video = Video.query.get(self.video_id)
        return {
            "video_id": self.video_id,
            "title": video.title,
            "customer_id": self.customer_id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "checkout_date": self.checkout_date,
            "due_date": self.due_date,
            "check_in_date": self.check_in_date
            }
    
    def video_history_to_json(self):
        customer = Customer.query.get(self.customer_id)
        return {
            "customer_id": self.customer_id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "checkout_date": self.checkout_date,
            "due_date": self.due_date,
            "check_in_date": self.check_in_date
            }
    
    def customer_history_to_json(self):
        video = Video.query.get(self.video_id)
        return {
            "title": video.title,
            "checkout_date": self.checkout_date,
            "due_date": self.due_date,
            "check_in_date": self.check_in_date
            }