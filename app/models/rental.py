from flask import current_app
from app import db
# from datetime import datetime, timedelta 


class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'))
    due_date = db.Column(db.DateTime, nullable=True, default=None)
    #alternate default for due_date: default=(datetime.now()+timedelta(days=7))


    # def to_dict(self):
    #     return {
    #         "id": self.video_id, 
    #         "title": self.title,
    #         "release_date": self.release_date,
    #         "total_inventory": self.total_inventory,
    #         "available_inventory": self.available_inventory,
    #         }