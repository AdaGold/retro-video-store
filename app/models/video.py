from flask import current_app
from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    release_date = db.Column(db.String)
    total_inventory= db.Column(db.Integer)
