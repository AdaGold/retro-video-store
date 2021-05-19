from flask import current_app
from app import db
from datetime import datetime
# from .rentals import Rentals


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable=True)
    postal_code = db.Column(db.String)
    # checked_out = db.relationship('Video', 
    #     secondary=Rentals, 
    #     back_populates='rented_to')

    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "phone" : self.phone,
            "registered_at" : self.register_at,
            "postal_code" : self.postal_code,
            "videos_checked_out_count" : 0
        }