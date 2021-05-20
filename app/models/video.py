from flask import current_app
from app import db
from sqlalchemy.orm import relationship

class Video(db.Model):
    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer) #, default=1)
    customer = relationship("Rental", back_populates="video")

    def to_json(self):
        # self.available_inventory = self.total_inventory
        video_json = {
            "id": self.id,
            "title": self.title, 
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }
        # if self.available_inventory:
        #     video_json["available_inventory"] = self.available_inventory
        return video_json


