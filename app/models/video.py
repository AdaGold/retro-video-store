from flask import current_app
from app import db
from sqlalchemy.orm import relationship


class Video(db.Model):
    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    customer = relationship("Rental", back_populates="video")

    def to_json(self):
        video_dict = {
            "video_id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
        }
        return video_dict