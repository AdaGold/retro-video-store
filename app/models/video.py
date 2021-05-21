from flask import current_app
from app import db
from datetime import datetime

class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    # Establish many-many relationship with Customers

    def get_video_data_structure(self):
        video_data_structure = {
                    "id":self.id,
                    "title":self.title,
                    "release_date": self.release_date.strftime("%Y-%m-%d"),
                    "total_inventory": self.total_inventory,
                    "available_inventory": self.available_inventory
                }
                

        return video_data_structure
