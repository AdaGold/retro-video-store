from flask import current_app
from sqlalchemy.orm import relationship 
from app import db 

class Video(db.Model):
    __tablename__ = "videos"
    video_id = db.Column(db.Integer, primary_key=True)
    video_title = db.Column(db.String(120))
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer) 
    available_inventory = db.Column(db.Integer)
    customers = relationship("Rental", back_populates="video")


    def to_json(self):
            video_dictionary = { "id": self.video_id, 
                                    "title": self.video_title, 
                                    "release_date": self.release_date, 
                                    "total_inventory": self.total_inventory
                                    # "available_inventory": self.available_inventory
                                    }
            return video_dictionary


    # @classmethod
    # def new_video_from_json(cls, body):
    #     new_video = Video(video_title=body["title"], release_date=body["release_date"], total_inventory=body["total_inventory"])

    #     return new_video

