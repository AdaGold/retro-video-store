from flask import current_app
from sqlalchemy.orm import backref
from app import db
from datetime import datetime


class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    video_check_out_count = db.Column(db.Integer)

    def to_json(self):
        
        # This method was created so that we do not have to write out the dictionary many times in the routes.py file.
        return {
                "id": self.customer_id,
                "name": self.name,
                "registered_at": self.registered_at,
                "postal_code": self.postal_code,
                "phone": self.phone,
                "video_check_out_count": self.video_check_out_count
            }