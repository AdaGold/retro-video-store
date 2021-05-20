from flask import current_app
from app import db
# from sqlalchemy.orm import relationship
from datetime import datetime

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime(), nullable=True)
    videos_checked_out_count = db.Column(db.Integer, nullable=True)
    
    rentals = db.relationship("Rental", backref="customer", lazy=True)

    def to_dict(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": datetime.now() if self.registered_at is None else self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": len(self.rentals),
        }
