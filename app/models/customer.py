from os import register_at_fork
from flask import current_app
from app import db

class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String)
    register_at = db.Column(db.DateTime)

    def customer_response(self):
        customer_dictionary={
            "id": self.customer_id,
            "name": self.customer_name,
            "registered_at": self.register_at,
            "postal__code": self.postal_code,
            "phone": self.phone_number
        }
        return customer_dictionary