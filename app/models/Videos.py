from flask import current_app
from app import db 

class Video(db.Model):
    __tablename__ = "videos"
    video_id = db.Column(db.Integer, primary_key=True)
    video_title = db.Column(db.String(120))
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer) 
