from flask import current_app
from app import db
from sqlalchemy.orm import relationship

class Video(db.Model):
    __tablename__ = 'video'
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title_of_video = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.String)
    
