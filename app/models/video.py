from flask import current_app
from app import db

def mydefault(context):
        return context.get_current_parameters()['total_inventory']

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    total_inventory = db.Column(db.Integer, nullable=False, default=0)
    available_inventory = db.Column(db.Integer, nullable=False, default=mydefault)
    
    def json_response(self):
        response = {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
            }

        return response