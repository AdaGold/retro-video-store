from flask import current_app
from app import db
from datetime import datetime

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False) 
    available_inventory = db.Column(db.Integer, nullable=False) 

    def video_to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "release_date": (False if self.release_date == None else True),
            "total_inventory": (False if self.total_inventory == None else True),
            "available_inventory": (False if self.available_inventory == None else True)
            }