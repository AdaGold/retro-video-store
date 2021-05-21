from flask import current_app
from sqlalchemy.orm import backref
from app import db
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.orm import relation, relationship

class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    postal_code = db.Column(db.String)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow())
    # videos_checked_out_count = db.Column(db.Integer, default=0)
    # creates a list of checked out videos
    videos = db.relationship('Video', back_populates='customers', secondary='rentals')
    # rentals = db.relationship('Rental', backref='rental', lazy=True)

    def to_json(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "phone": self.phone,
            "postal_code": self.postal_code,
            "registered_at": self.registered_at,
            # index_checked_out function can be called to show checkout count
            "videos_checked_out_count": self.index_checked_out()
        }
    # returns the length (amount) of checked out videos, via videos list
    def index_checked_out(self):
        return len(self.videos)