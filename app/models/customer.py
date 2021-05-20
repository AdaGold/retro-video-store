from datetime import datetime
from flask import current_app
from app import db

class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)

    def customer_response(self):
        if self.register_at:
            registered = datetime.datetime(self.register_at)
        else:
            registered = None
        customer_dictionary={
            "id": self.customer_id,
            "name": self.name,
            "registered_at": registered,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count
        }
        return customer_dictionary