from flask import current_app
from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    # available_inventory = db.Column(db.Integer)

    def to_json(self):
        """
        Outputs formatted JSON dictionary of video attributes
        """
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
            # "available_inventory": self.available_inventory
            }

    def from_json(self, input_data):
        """
        Converts JSON input data into new instance of Video
        """
        return self(title=input_data["title"],
        release_date=input_data["release_date"],
        total_inventory=input_data["total_inventory"])
