from flask import current_app
from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    #available inventory

    def json_response(self):
        response = {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
            #available_inventory: 1
            }

        return response