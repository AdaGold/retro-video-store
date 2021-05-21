from flask import current_app
from app import db
from datetime import datetime

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False)
    #available_inventory = db.Column(db.Integer, nullable=False)
    #establish relationship with customer
    rentals = db.relationship('Rental', backref='video', lazy=True)
    
    def calculate_available_inventory(self):
        available_inventory = self.total_inventory - len(self.rentals)
        return available_inventory
        
    def video_details(self):
        return  {
                    "id": self.video_id,
                    "title": self.title,
                    "release_date": self.release_date,
                    "total_inventory": self.total_inventory,
                    "available_inventory":self.calculate_available_inventory() #wave 2
                    #"available_inventory": self.calculate_available_inventory() #wave 1
                }
  