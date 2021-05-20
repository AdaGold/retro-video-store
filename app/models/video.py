from flask import current_app
from app import db
from sqlalchemy import DateTime

def get_total_inventory(context):
    return context.get_current_parameters()['total_inventory']

class Video(db.Model):
    __tablename__ = 'videos'

    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer, default=get_total_inventory)
    
    customers = db.relationship("Customer", secondary="rentals", back_populates="videos")
    
    def to_json(self):
        video = {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }
        return video