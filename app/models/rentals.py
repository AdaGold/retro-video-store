from flask import current_app
from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), primary_key=True)
    checkout_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    check_in_date = db.Column(db.DateTime, nullable=True, default=None)
    customer = db.relationship("Customer", back_populates="videos")
    video = db.relationship("Video", back_populates="customers")
    __tablename__ = "rentals"

    def check_out_to_json(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
            }
    
    def check_in_to_json(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
            }
    
    def overdue_to_json(self):
        return {
            "video_id": self.video_id,
            "title": self.video.title,
            "customer_id": self.customer_id,
            "name": self.customer.name,
            "postal_code": self.customer.postal_code,
            "checkout_date": self.checkout_date,
            "due_date": self.due_date
            }
    
    def video_history_to_json(self):
        return {
            "customer_id": self.customer_id,
            "name": self.customer.name,
            "postal_code": self.customer.postal_code,
            "checkout_date": self.checkout_date,
            "due_date": self.due_date
            }
    
    def customer_history_to_json(self):
        return {
            "title": self.video.title,
            "checkout_date": self.checkout_date,
            "due_date": self.due_date,
            }