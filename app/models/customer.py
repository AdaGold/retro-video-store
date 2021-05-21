from flask import current_app
from app import db
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    
    rentals = db.relationship('Rental', backref='customers', lazy=True)

    def get_response(self):
        return {
            "id":self.id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": int(self.postal_code),
            "phone": self.phone,
            "videos_checked_out_count": len(self.rentals)}