from datetime import datetime
from flask import current_app
from app import db

class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, default=datetime.now(), nullable=True)
    videos_checked_out_count = db.Column(db.Integer, default=0)

    def customer_response(self):
        customer_dictionary={
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.register_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count
        }
        return customer_dictionary