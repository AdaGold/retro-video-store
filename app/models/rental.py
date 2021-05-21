from flask import current_app
from app import db
import datetime




class Rental(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime)



    def display_json(self):
        return {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "due_date" : self.due_date
        }
