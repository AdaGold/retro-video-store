from flask import current_app
from app import db


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.Integer)
    register_at = db.Column(db.DateTime)

    def build_dict(self):
        return {
            "id" : self.customer_id,
            "name" : self.name,
            "phone" : self.phone,
            "register_at" : self.register_at
        }
