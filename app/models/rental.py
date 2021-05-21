from flask import current_app
from sqlalchemy.orm import relation, relationship
from app import db
from sqlalchemy import DateTime
from .customer import Customer
from .video import Video

"""
rental attributes:
id
customer_id
video_id
due_date
"""
class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'))
    video_id = db.Column(db.Integer, db.ForeignKey('Video.video_id'))
    due_date = db.Column(db.DateTime)
    customer = relationship('Customer', backref=('customer_id'))

    def to_json(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.customer.videos_checked_out_count
        }

    