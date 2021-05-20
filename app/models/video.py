from flask import current_app
from app import db

class Video(db.Model):
    __tablename__ = "video"
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)

    customers = db.relationship("Customer", secondary="rental", backref="video", lazy=True)

    def to_json_video(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }