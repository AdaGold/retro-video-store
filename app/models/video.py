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


