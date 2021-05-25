from flask import current_app
from sqlalchemy.orm import backref
from app import db
from datetime import datetime, timedelta


class Rental(db.Model):
    __tablename__ = 'rental'
    rental_id = db.Column(db.Integer, primary_key = True, autoincrement=True )
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True)
    due_date = db.Column(db.DateTime, nullable = True)

    # def to_json(self):
        
    #     # This method was created so that we do not have to write out the dictionary many times in the routes.py file.
    #     return {
    #             "id": self.customer_id,
    #             "name": self.name,
    #             "registered_at": self.registered_at,
    #             "postal_code": self.postal_code,
    #             "phone": self.phone,
    #             "videos_checked_out_count": self.videos_checked_out_count
    #         }