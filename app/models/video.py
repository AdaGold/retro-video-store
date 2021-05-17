from flask import current_app
from app import db


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    total_copies = db.Column(db.Integer)
