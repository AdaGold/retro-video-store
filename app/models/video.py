from flask import current_app
from app import db
from datetime import datetime

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.date(), nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    
  
    customer_vids = db.relationship('customer_vids', secondary='Link', backref=db.backref('videos', lazy=True))