from flask import current_app
from app import db
from datetime import datetime

class Rental(db.Model):
    id = Column(Integer, primary_key=True),
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id')),
    video_id = db.Column(db.Integer, db.ForeignKey('video.id')),
    due_date = db.Column(db.DateTime, nullable=True, default=((datetime.today) + (datetime.timedelta(days=7))))