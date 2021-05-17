from datetime import datetime
from flask import current_app
from app import db
from datetime import datetime


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(
        db.DateTime,
        nullable=True,
        default=datetime.now())

    def to_json(self):
        """Converts a Customer instance into JSON"""
        response_body = {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at
        }
        return response_body

    def from_json(self, json):
        """Converts JSON into a new instance of Customer"""
        self.name = json["name"]
        self.postal_code = json["postal_code"]
        self.phone = json["phone"]
        # self.registered_at = json["registered_at"]
        return self
