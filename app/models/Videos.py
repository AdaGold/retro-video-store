from flask import current_app
from sqlalchemy.orm import relationship 
from app import db 

def default_value(video):
    return video.get_current_parameters()["total_inventory"]

class Video(db.Model):
    __tablename__ = "videos"
    video_id = db.Column(db.Integer, primary_key=True)
    video_title = db.Column(db.String(120))
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer) 
    available_inventory = db.Column(db.Integer, default=default_value)
    # customers = relationship("Rental", back_populates="video")


    def to_json(self):
        video_dictionary = { "id": self.video_id, 
                                "title": self.video_title, 
                                "release_date": self.release_date, 
                                "total_inventory": self.total_inventory,
                                "available_inventory": self.available_inventory
                                }
        return video_dictionary



