from flask import current_app
from app import db
from flask import request, Blueprint, make_response, jsonify

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.Integer)
    register_at = db.Column(db.DateTime, nullable = True)