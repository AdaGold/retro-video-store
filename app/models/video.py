from flask import current_app
from app import db
from sqlalchemy.orm import relationship

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable = True)
    inventory = db.Column(db.Integer)