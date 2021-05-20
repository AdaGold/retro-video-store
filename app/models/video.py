from flask import current_app
from app import db
from sqlalchemy import DateTime


class Video(db.Model):
    __tablename__ = 'videos'

    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer", secondary="rentals", back_populates="videos")
    
    def to_json(self):
        video = {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.get_available_inventory()
        }
        return video

    def get_available_inventory(self):
        return self.total_inventory - len(self.customers)
        