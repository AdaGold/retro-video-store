from flask import current_app
from app import db 
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship 

class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    videos = relationship("Rental", back_populates="customer")
    #customer.videos -> array of all videos they have checked out 

    def to_json(self): 
        serialized = {     
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone, 
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }

        return serialized