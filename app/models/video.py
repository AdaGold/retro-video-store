
from flask import current_app
from app import db
from datetime import datetime


class Video(db.Model):
    __tablename__ = "videos"
    video_id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)

    def resp_json(self):
        if self.release_date:
            release_date = datetime.date(self.release_date)
        video_info = {
            "id": self.video_id,
            "title": self.title,
            "release_date": release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
            }
        return video_info
        