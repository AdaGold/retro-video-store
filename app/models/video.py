from flask import current_app
from flask.helpers import make_response
from app import db
from sqlalchemy import DateTime

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer, default=0)

    def to_json(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }
    
    def decrease_inventory(self):
        if self.available_inventory == 0:
            return make_response("No inventory left!", 400)
        else:
            self.available_inventory -= 1
            db.session.commit()