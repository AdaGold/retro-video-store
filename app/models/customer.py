# Customers are entities that describe a customer at the video store. 
# They contain:

# name of the customer
# postal code of the customer
# phone number of the customer
# register_at datetime of when the customer was added to the system.

from flask import current_app
from app import db

class Customer(db.Model):
    name = db.Column(db.String, primary_key=True)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    completed_at = db.Column(db.DateTime, nullable = True)


    def complete_task(self):
        if self.completed_at == None:
            return False
        else: 
            return True