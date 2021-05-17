from flask import current_app
from app import db
from datetime import datetime
#from sqlalchemy import PhoneNumber
from sqlalchemy_utils import PhoneNumber
import phonenumbers



class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String) 
    register_at = db.Column(db.DateTime, nullable=False)
    
    #establish relationship
    videos_checked_out = db.relationship('Video', secondary='Link', backref=db.backref('customers', lazy=True))

    def list_of_customer_response(self):
        return {
                "id": self.customer_id,
                "name": self.name,
                "registered_at": self.register_at,
                "postal_code": self.postal_code,
                "phone": self.phone_number,
                "videos_checked_out_count": self.videos_checked_out
                }