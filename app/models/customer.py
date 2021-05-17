from flask import current_app
from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        """
        Outputs formatted JSON dictionary of customer attributes
        """
        return {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at
            }

    def from_json(self, input_data):
        """
        Converts JSON input data into new instance of Customer
        """
        return self(name=input_data["name"],
        postal_code=input_data["postal_code"],
        phone=input_data["phone"],
        registered_at=input_data["registered_at"])
