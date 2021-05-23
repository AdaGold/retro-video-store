from app import db
import datetime
from flask import current_app
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# this is telling flask about my database task table


class Rental(db.Model):
    # One primary key per a model
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'))
    
    due_date = db.Column(db.DateTime, default=(datetime.datetime.now()) + (datetime.timedelta(days=7)))

    # variables to connect video & customer object to rental
    rental_video_relationship = relationship("Video", backref="rentals")
    rental_customer_relationship = relationship("Customer", backref="rentals")

    def json_object(self):

        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.rental_customer_relationship.videos_checked_out_count,
            "available_inventory": self.rental_video_relationship.available_inventory
        }
