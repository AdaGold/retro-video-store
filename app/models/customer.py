# Customers are entities that describe a customer at the video store. 
# They contain:

# name of the customer
# postal code of the customer
# phone number of the customer
# register_at datetime of when the customer was added to the system.

from flask import current_app
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    register_at = db.Column(db.DateTime, nullable = True)
    checkout_count = db.Column(db.Integer, default =0) #why do I need this here?


    def registered_customer(self):
        if self.register_at == None:
            return False
        else: 
            return True

#helper function 
    def to_json_customer(self):
        return {
        "id": self.id,
        "name": self.name,
        "postal_code": self.postal_code,
        "register_at": self.register_at, # or self.registered_customer()
        "checkout_count": self.checkout_count
        }
