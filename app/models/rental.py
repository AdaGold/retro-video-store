from flask import current_app
from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.DateTime, nullable=True)

    def rental_to_json(self, customer, video):
        return {
            "customer_id":self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date
        }

