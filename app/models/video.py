from flask import current_app
from app import db

# def default_avail_inv(context): 
#     return context.get_current_parameters()["total_inventory"]

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    # available_inventory = db.Column(db.Integer, default=default_avail_inv)
    available_inventory = db.Column(db.Integer)

    def to_json(self): 
        to_json = {
                "id": self.video_id,
                "title": self.title,
                "released_date": self.release_date,
                "total_inventory": self.total_inventory, 
                "available_inventory": self.available_inventory            
        }
        return to_json
    
    @classmethod
    def make_a_video(cls, json, id): 
        return cls(video_id=id,
                    title=json["title"],
                    release_date=json["release_date"], 
                    total_inventory=json["total_inventory"])