from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.models.video import Video

Base = declarative_base()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    created = db.Column(db.DateTime, nullable=True, default=None)
    #do i need the db. before relationships? what i saw online didnt have it
    videos = db.relationship("Rental", back_populates="rentals")
    __tablename__ = "Customer"
    # video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=True) 

    # def calc_videos_checked_out():
    #     pass

    def api_response(self): 
        response_body = {
                        "id": self.id,
                        "name": self.name,
                        #below needs to change
                        "registered_at": self.created,
                        "postal_code": self.postal_code,
                        "phone": self.phone,
                        #below needs to change
                        "videos_checked_out_count": 0
                        # "videos_checked_out_count": calc_videos_checked_out()
                        }

        return response_body
