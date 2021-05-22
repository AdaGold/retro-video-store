from flask import current_app
from app import db
import datetime 


class Video(db.Model): 
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer, default=0)
    available_inventory = db.Column(db.Integer, default=1)
    rentals = db.relationship("Rental", back_populates="video")
    
    def to_json(self):
        r_date = self.release_date.date()
        r_date = r_date.isoformat()

        regular_response = {

            "id": self.video_id,
            "title": self.title,
            "release_date": r_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }
        return regular_response 