from flask import current_app
from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True, default=None)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)

    def vid_details(self):
        return {
        "id": self.video_id,
        "title": self.title,
        "release_date": self.release_date,
        "total_inventory": self.total_inventory}

    def check_out(self):
        self.available_inventory -= 1
        db.session.commit()

    def check_in(self):
        self.available_inventory += 1
        db.session.commit()