# from flask import current_app
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)