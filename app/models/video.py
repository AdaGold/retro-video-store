from flask import current_app
from app import db

class Video(db.Model):
    __tablename__ = "video"
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    inventory = db.Column(db.Integer)

    def video_response(self):
        video_dictionary={
            "id": self.video_id,
            "title": self.video_title,
            "release_date": self.release_date,
            "total_inventory": self.inventory
        }
        return video_dictionary