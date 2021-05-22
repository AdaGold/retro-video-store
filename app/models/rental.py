from flask import current_app
from app import db
from datetime import datetime, date, timedelta
from sqlalchemy.orm import relationship, backref

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True)
    due_date = db.Column(db.DateTime, default=(datetime.now() + timedelta(days=7)))

    customer = relationship("Customer", backref='video', lazy=True)
    video = relationship("Video", backref='customer', lazy=True)

    def rental_info(self):
        return {
            "rental_id": self.rental_id,
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date
            }
