from flask import current_app
from app import db
from datetime import datetime
from app.models.rental import Rental

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    videos_checked_out_count = db.Column(db.Integer, nullable = False, default=0)
    rentals_out = db.relationship("Rental", backref="customer") #is lazy=True needed?

    def return_data(self):
        return_info = {
                "id": self.id,
                "name": self.name,
                "registered_at": self.register_at,
                "postal_code": self.postal_code,
                "phone": self.phone,
                "videos_checked_out_count": self.videos_checked_out_count
            }
        return return_info