from flask import current_app
from app import db
from dataclasses import dataclass 
from datetime import datetime


@dataclass
class Customer(db.Model):
    id: int 
    name: str 
    postal_code: int
    phone: str
    registered_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    
def as_json(self):

        result_dict = {
                "id": self.id,
                "name": self.name,
                "registered_at": self.registered_at,
                "postal_code": self.postal_code,
                "phone": self.phone,
                "videos_checked_out_count": self.videos_checked_out,

            }

        return result_dict