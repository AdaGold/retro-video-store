from flask import current_app
from app import db

class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer)
    # Establish many-many relationship with Videos
