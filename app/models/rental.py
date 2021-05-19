from flask import current_app
from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    __tablename__ = 'rental'
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True)
    due_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    
    @classmethod  
    def from_json(cls, json_file):
        return cls(**json_file)