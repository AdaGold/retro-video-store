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
    video = db.relationship("Video", backref="rental")
    customer = db.relationship("Customer", backref="rental")

    def json_object(self):

        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
        }
