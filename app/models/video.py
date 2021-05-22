from flask import current_app
from app import db
from sqlalchemy.orm import relationship


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    # declare relationship between customer and rental here ?
    videos = db.relationship("Rental", backref="videos", lazy=True)


    def to_json_video(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory, 
            }   
            # 
            # "available_inventory":self.available_inventory 
            # deleted this addition and my tests were now passing 
            # "available_inventory":self.add a helper function here that will subtract total inventory - customer where does this even go ???