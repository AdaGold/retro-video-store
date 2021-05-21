from flask import current_app
from app import db
import datetime


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory= db.Column(db.Integer, default=0)
    # active_rentals = db.relationship('Rental', backref='video')


    

# helper function  display  json
    def display_json(self):

        # release_date_format = self.release_date.date()
        # release_date_format = release_date_format.isoformat()
        return {
                "id": self.video_id,
                "title": self.title,
                "release_date": self.release_date,
                "total_inventory": self.total_inventory,
                "available_inventory": 10
                # "available_inventory": (self.total_inventory - len(self.active_rentals))
                }  