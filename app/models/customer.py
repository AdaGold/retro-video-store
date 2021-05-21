from app.models import rentals
from flask import current_app
from app import db
from datetime import datetime

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String(200))
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String(12)) 
    register_at = db.Column(db.DateTime) 
    videos_checked_out_count = db.Column(db.Integer, default=0)
    # becca: make the same as goals and tasks relationships
    #rental = db.relationship('Rental', backref='rental', lazy=True)

    def to_json(self):
        if self.register_at:
            check_registration = True
        else:
            check_registration = False
        
        return {
            "id": self.customer_id,
            "name": self.name,
            "phone": self.phone_number,
            "postal_code": self.postal_code,
            "registered_at": check_registration,
            "videos_checked_out_count": self.videos_checked_out_count
            }

