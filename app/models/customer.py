from flask import current_app
from app import db
from sqlalchemy import DateTime
from app.models import customer_video_join  


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone_number = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable=True)
    videos = db.relationship("Video", secondary=customer_video_join)
    