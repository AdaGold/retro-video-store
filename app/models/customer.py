from flask import current_app
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    rental_info = db.relationship('Rental', backref='customers', lazy=True)

    def to_json(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.register_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }