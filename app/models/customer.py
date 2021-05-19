from flask import current_app
from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True, default=None)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    
    def get_video_count(self):
        rentals = Rental.query.filter_by(customer_id = self.customer_id)
        checked_out = len(rentals)
        return checked_out

    def cust_details(self):
        return {
        "id": self.customer_id,
        "name": self.name,
        "registered_at": self.registered_at,
        "postal_code": self.postal_code,
        "phone": self.phone,
        "videos_checked_out_count": 0}