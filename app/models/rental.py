from flask import current_app
from app import db
from datetime import datetime

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer)
    video_id = db.Column(db.Integer)
    due_date = db.Column(db.DateTime, default=datetime.utcnow() - datetime.timedelta(days=7)) #need to set time to 7 days in future
