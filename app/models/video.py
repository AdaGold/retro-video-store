# Videos are entities that describe a video at the video store. They contain:

# title of the video
# release date datetime of when the video was release_date
# total inventory of how many copies are owned by the video store

from flask import current_app
from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable = True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer, default=0)
    rentals = db.relationship('Rental', backref = 'video')

#helper function 
    def to_json_video(self):
        return {
        "id": self.id,
        "title": self.title,
        "release_date": self.release_date,
        "total_inventory": self.total_inventory,
        "available_inventory": self.available_inventory
        }
