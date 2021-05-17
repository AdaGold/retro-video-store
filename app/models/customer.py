from flask import current_app
from app import db


class Customer(db.Model):
    """
    Attributes:
        name 
        postal code
        phone 
        registered_at
    """
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String,nullable=False)#required attributes
    postal_code = db.Column(db.String,nullable=False)#required attributes
    phone = db.Column(db.String,nullable=False)#required attributes
    registered_at = db.Column(db.DateTime,nullable=True)

    def to_python_dict(self):
        """
            Input: instance of Customer
            Output: returns a python dictionary of Customer instance

        """
        return {
            "customer_id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at
        }
