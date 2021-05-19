from flask import current_app
from app import db
from datetime import datetime

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "due_date" : self.due_date
        }

