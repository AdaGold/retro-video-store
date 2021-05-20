from flask import current_app
from app import db
from datetime import datetime, timedelta


class Rental(db.Model):
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"))
    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"))
    due_date = db.Column(db.DateTime, nullable=True, default = datetime.now() + timedelta(days=7))

