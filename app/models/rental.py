from flask import current_app
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rental(db.Model):
    __tablename__ = "rental"
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id", primary_key=True)) 
    video_id = db.Column(db.Integer, db.ForeignKey("video.video_id"), primary_key=True)

    def to_json_rental(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.customer_id.registered_at,
            "videos_checked_out_count": self.customer_id.videos_checked_out_count,
            "available_inventory": self.customer_id.available_inventory
        }