from flask import current_app
from app import db
from datetime import timedelta, datetime
import datetime 

class Video(db.Model): 
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer, default=0)
    available_inventory = db.Column(db.Integer, default=1)
    rentals = db.relationship("Rental", back_populates="video") # Relationship to rentals
    
    def to_json(self):


        regular_response = {

            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date.date.isoformat(),
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }
        return regular_response 