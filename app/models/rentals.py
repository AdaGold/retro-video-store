from flask import current_app
from app import db
from sqlalchemy import func
from datetime import timedelta


class Rental(db.Model):
    __tablename__ = 'rental'
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    extra_data = db.Column(db.DateTime, server_default=func.now() + timedelta(days=7))
    videos = db.relationship("Video", backref="rental", lazy=True)
    customers = db.relationship("Customer", backref="rental", lazy=True) 