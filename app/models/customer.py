from flask import current_app
from app import db
from datetime import datetime

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    # videos_checked_out_count = db.Column(db.Integer, default=0)
    # rentals = db.relationship('Rental', back_populates='customer', lazy=True)
    
    def customer_to_json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "phone" : self.phone,
            "registered_at" : self.register_at,
            "postal_code" : self.postal_code,
            # "videos_checked_out_count" : len(self.current_rentals)
        }
