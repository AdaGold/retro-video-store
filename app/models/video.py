from flask import current_app
from app import db
from datetime import datetime
from sqlalchemy.orm import relationship 


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer, default=0) 
    available_inventory = db.Column(db.Integer, default=total_inventory) 
    # rentals = db.relationship('Rental', back_populates='video', lazy=True)

    def video_to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
            }