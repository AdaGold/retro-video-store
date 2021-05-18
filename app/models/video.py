from flask import current_app
from app import db
from datetime import datetime

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name =  db.Column(db.String)
    release_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    total_inventory = db.Column(db.Integer)

    def to_json(self):
        return{
            "id": self.customer_id,
            "name": self.name,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }