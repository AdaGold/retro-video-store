from flask import current_app
from app import db

class Rental(db.Model):
    __tablename__ = 'rental'
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rental_customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    rental_video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True)
    due_date = db.Column(db.DateTime, nullable=True)