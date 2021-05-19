from flask import current_app
from app import db
from sqlalchemy.orm import relationship

class Video(db.Model):
    __tablename__ = 'video'
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title_of_video = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    

    def v_json_response(self):
        return {
            "id": self.video_id,
            "title": self.title_of_video,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": 0

        }
