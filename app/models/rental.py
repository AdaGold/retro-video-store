from flask import current_app
from app import db
from datetime import datetime

class Rental(db.Model):
    __tablename__ = 'rental'
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    child = db.relationship("Video", back_populates="Customer")
    parent = db.relationship("Customer", back_populates="Video")