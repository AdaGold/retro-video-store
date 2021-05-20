from flask import current_app
from app import db
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship
# from .customer import Customer
# from .video import Video
from datetime import timedelta

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # a foreign key column refers to the primary key of the other table
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=True, default=None) #nullable=True means Null is allowed in this column
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), nullable=True, default=None)
    due_date = db.Column(db.Date(), nullable=True)


    def to_dict(self):
        return {
            "rental_id": self.rental_id,
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date + timedelta(days=7),
        }