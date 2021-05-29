from flask import current_app
from app import db
from datetime import datetime
from sqlalchemy.orm import backref

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    phone_number = db.Column(db.String(12))
    postal_code = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime, nullable = True, default = None)
    videos_checked_out_count = db.Column(db.Integer, autoincrement=False, default=0)
    rentals = db.relationship('Rental', back_populates='customer', lazy=True)

    def customer_info(self):
            return {
                "id": self.customer_id,
                "name": self.name,
                "phone": self.phone_number,
                "postal_code": self.postal_code,
                "registered_at": self.registered_at,
                "videos_checked_out_count": self.videos_checked_out_count
                } 

