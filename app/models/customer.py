from flask import current_app
from app import db
from datetime import datetime
# from .rentals import Rentals


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    phone_number = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable=True)
    post_code = db.Column(db.String)
    # checked_out = db.relationship('Video', 
    #     secondary=Rentals, 
    #     back_populates='rented_to')

    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "register_at" : self.register_at,
            "post_code" : self.post_code,
            "videos_checked_out_count" : 0
        }