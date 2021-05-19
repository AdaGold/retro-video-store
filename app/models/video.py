from flask import current_app
from app import db
from datetime import datetime

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    #available_inventory = db.Column(db.Integer, nullable=False)

    def calculate_available_inventory(self):
            pass
        
    def video_details(self):
        return  {
                    "id": self.video_id,
                    "title": self.title,
                    "release_date": self.release_date,
                    "total_inventory": self.total_inventory,
                    #"available_inventory": self.calculate_available_inventory()
                }
  
#     customer_vids = db.relationship('customer_vids', secondary=association_table, backref=db.backref('videos', lazy=True))