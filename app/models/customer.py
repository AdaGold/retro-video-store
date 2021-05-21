from flask import current_app
from app import db
from flask_sqlalchemy import SQLAlchemy


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone_num = db.Column(db.String)
    register_at = db.Column(db.Datetime)


# - name of the customer
# - postal code of the customer
# - phone number of the customer
# - register_at datetime of when the customer was added to the system.
