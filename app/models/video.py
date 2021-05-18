from flask import current_app
from app import db
from sqlalchemy import DateTime
from app.models import customer_video_join  

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer", secondary=customer_video_join)
