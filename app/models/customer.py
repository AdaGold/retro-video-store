
from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# two col table that points to both models
rentals = db.Table('rentals',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.customer_id')),
    db.Column('video_id', db.Integer, db.ForeignKey('video.video_id')),
    )

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True, default=None)
    postal_code = db.Column(db.String)
    phone_number = db.Column(db.String)
    # connect to rentals table
    check_outs = db.relationship('Video', secondary='rentals', backref='customers', lazy=True)


    def get_response(self):
        return {
            "id":self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone_number,
            "videos_checked_out_count": int(self.check_outs)}