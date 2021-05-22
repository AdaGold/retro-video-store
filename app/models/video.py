from flask import current_app
from app import db
import datetime


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory= db.Column(db.Integer, default=0)
    available_inventory = db.Column(db.Integer, default=0)
    # making a relationship between rentals and video 
    rentals = db.relationship("Rental", back_populates="video")
    

    

# helper function  display  json
    def display_json(self):

    
        return {
                "id": self.video_id,
                "title": self.title,
                "release_date": self.release_date,
                "total_inventory": self.total_inventory,
                "available_inventory": self.inventory
                }  