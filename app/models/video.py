from flask import current_app
from datetime import datetime
from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable = True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    # customers = db.relationship("Customer", backref='video', lazy=True)


    def to_json(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
            }
