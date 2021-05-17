from flask import current_app
from app import db


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime, nullable=True)

