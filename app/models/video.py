from flask import current_app
from app import db
from datetime import datetime


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    release_date = db.Column(
        db.DateTime,
        nullable=True,
        default=datetime.now())

    def to_json(self):
        """Converts a Video instance into JSON"""
        response_body = {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }
        return response_body

    def from_json(self, json):
        """Converts JSON into a new instance of Video"""
        self.title = json["title"]
        self.total_inventory = json["total_inventory"]
        self.available_inventory = json["available_inventory"]
        self.release_date = json["release_date"]
        return self
