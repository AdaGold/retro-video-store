from flask import current_app
from sqlalchemy.orm import backref
from app import db
from datetime import datetime


class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime, default = datetime.now())
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer, default = 0)

    def to_json(self):
        
        # This method was created so that we do not have to write out the dictionary many times in the routes.py file.
        return {
                "id": self.customer_id,
                "name": self.name,
                "registered_at": self.registered_at,
                "postal_code": self.postal_code,
                "phone": self.phone,
                "videos_checked_out_count": self.videos_checked_out_count
            }