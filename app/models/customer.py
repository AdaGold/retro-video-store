from flask import current_app
from app import db


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out_count = db.Column(db.Integer, default=0)

    rentals = db.relationship("Rental", backref="customer", lazy=True)

    def to_dict(self):
        return {
            "id": self.customer_id, 
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count
            }
    
    def check_out(self):
        self.videos_checked_out_count += 1
    
    def check_in(self):
        self.videos_checked_out_count -= 1