from flask import current_app
from app import db


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    total_inventory = db.Column(db.Integer, default = 0)
    # declare relationship between customer and rental here



    def to_json_video(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            }   
            # "available_inventory":self.add a helper function here that will subtract total inventory - customer where does this even go ???