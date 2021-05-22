from app import db 
from flask import current_app
from sqlalchemy.orm import relationship 


class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"))
    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"))
    due_date = db.Column(db.DateTime)

    # customer = relationship("Customer", back_populates="videos")
    # video = relationship("Video", back_populates="customers")


    def to_json(self):
        return {
            "release_date": self.video.release_date, 
            "title": self.video.title, 
            "due_date": self.due_date
        }