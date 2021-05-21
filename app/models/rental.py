from flask import current_app
from app import db

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    due_date = db.Column(db.DateTime, nullable=True, default=None)