from flask import current_app
from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Rental(db.Model):
    __tablename__ = "rental"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column("customer", db.Integer, db.ForeignKey("customer.id"), primary_key=True)
    video_id = db.Column("video", db.Integer, db.ForeignKey("video.id"), primary_key=True)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String)
    video = relationship("Video", back_populates="customer")
    customer = relationship("Customer", back_populates="video")

    def to_json(self):

        rental_json = {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date
        }
