from flask import current_app
from app import db 
from sqlalchemy.orm import relationship
from datetime import datetime



class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(64))
    customer_zip = db.Column(db.String(5))
    customer_phone = db.Column(db.String(14))
    register_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)

    #curious about what this is doing and why it works w/o it 
    videos = relationship("Rental", back_populates="customer", cascade="all, delete")
    


    def to_json(self):
        return { 
            "id": self.customer_id, 
            "name": self.customer_name, 
            "postal_code": self.customer_zip, 
            "phone": self.customer_phone, 
            "registered_at": self.register_at, 
            "videos_checked_out_count": self.videos_checked_out_count,
                                }

    @classmethod
    def new_customer_from_json(cls, request_body):
        return Customer(customer_name=request_body["name"], customer_zip=request_body["postal_code"], customer_phone=request_body["phone"], register_at=datetime.now(), videos_checked_out_count=0)
