from sqlalchemy.orm import relationship, backref
from flask import current_app
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)

    registered_at = db.Column(db.DateTime, nullable = True)
    checkout_count = db.Column(db.Integer, default =0) 

    video = relationship("Rental", back_populates="customer")

    #helper function 
    def to_json_customer(self):
        return {
        "id": self.id,
        "name": self.name,
        "phone": self.phone,
        "postal_code": int(self.postal_code),
        "registered_at": self.registered_at, # or self.registered_customer()
        "videos_checked_out_count": self.checkout_count
        }
