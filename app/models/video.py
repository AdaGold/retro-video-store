from flask import current_app
from sqlalchemy.orm import backref
from app import db


class Video(db.Model):
    __tablename__ = 'video'
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)

    def to_json_video(self):
        
        # This method was created so that we do not have to write out the dictionary many times in the routes.py file.
        return {
                "id": self.video_id,
                "title": self.title,
                "release_date": self.release_date,
                "total_inventory": self.total_inventory,
                "available_inventory": self.available_inventory,
            }