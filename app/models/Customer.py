from app import db
from flask import current_app
from sqlalchemy import DateTime
from datetime import date, datetime, timedelta

class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    videos_rented = db.Column(db.Integer, default=0)
    rentals = db.relationship("Rental", backref="customers", lazy=True)
    

    def customer_info(self):
        if self.registered_at:
            is_registered = True
        else:
            is_registered = False

        return {
            "id": self.customer_id, 
            "name": self.name, 
            "postal_code": self.postal_code, 
            "phone": self.phone, 
            "registered_at": self.registered_at, 
            "videos_rented": self.videos_rented 
        }

    def check_out(self):
        self.videos_rented += 1
        self.save()

    def check_in(self):
        self.videos_rented -= 1
        self.save()