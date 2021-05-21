from flask import current_app
from app import db
from sqlalchemy import DateTime
from datetime import datetime, date, timedelta

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True)
    # due_date = db.Column(db.DateTime, default=(datetime.datetime.utcnow() + timedelta(days=7)))

    def rental_info(self):
        return {
            "rental_id": self.rental_id,
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date
            }
