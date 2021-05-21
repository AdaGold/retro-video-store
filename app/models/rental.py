from flask import current_app
from app import db
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship
# from .customer import Customer
# from .video import Video
from datetime import datetime, timedelta

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # a foreign key column refers to the primary key of the other table
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=True, default=None) #nullable=True means Null is allowed in this column
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), nullable=True, default=None)
    due_date = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(days=7))


    def rental_to_dict(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
        }