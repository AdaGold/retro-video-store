from flask import current_app
from app import db
from dataclasses import dataclass 



@dataclass
class Video(db.Model):
    id: int 
    title: str 
    release_date: int
    total_inventory: int 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Integer)
    total_inventory = db.Column(db.Integer)


def to_json(self):
    result_dict = {
            
            "id": 1,
            "title": "Blacksmith Of The Banished",
            "release_date": "1979-01-18",
            "total_inventory": 10,
            "available_inventory": 9
        }
    return result_dict