from app import db
from flask import current_app


class Video(db.Model):
    __tablename__ = "videos"
    video_id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True, default=None)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    rentals = db.relationship("Rental", backref="videos", lazy=True)

    def video_info(self):
        return {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }

    def check_in(self):
         self.available_inventory += 1
         

    def check_out(self):
         self.available_inventory -= 1
         

    def has_available_inventory(self):
        if self.available_inventory > 0:
            return True
        else:
            return False
