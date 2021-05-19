from flask import current_app
from app import db
from dataclasses import dataclass 



@dataclass
class Video(db.Model):
    id: int 
    title: str 
    release_date: str
    total_inventory: int 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    total_inventory = db.Column(db.Integer)


    def to_json(self):
        result_dict = {
            
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            #"available_inventory": 0
        }
        return result_dict


    @classmethod
    def from_json(cls,video_dict): 
        return Video(
            title = video_dict["title"],
            release_date = video_dict["release_date"],
            total_inventory = video_dict["total_inventory"],
    )