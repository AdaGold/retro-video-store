from flask import current_app
from app import db 

class Video(db.Model):
    __tablename__ = "videos"
    video_id = db.Column(db.Integer, primary_key=True)
    video_title = db.Column(db.String(120))
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer) 

    def to_json(self):
            video_dictionary = { "ID": self.video_id, 
                                    "Title": self.video_title, 
                                    "Release Date": self.release_date, 
                                    "Total Inventory": self.total_inventory, 
                                    }
            return video_dictionary


    @classmethod
    def new_video_from_json(cls, body):
        new_video = Video(video_title=body["title"], release_date=body["release_date"], total_inventory=body["total_inventory"])

        return new_video

