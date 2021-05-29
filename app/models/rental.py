from flask import current_app
from app import db
from datetime import datetime, date, timedelta
from sqlalchemy.orm import relationship

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'))
    due_date = db.Column(db.DateTime, default=(datetime.now() + timedelta(days=7)))

    # go back to the Customers class and bring it back to rentals
    customer = relationship("Customer", back_populates='rentals', lazy=True)
    video = relationship("Video", back_populates='rentals', lazy=True)

    def rental_info(self):
        return {
            "rental_id": self.rental_id,
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date
            }
