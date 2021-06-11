from flask import current_app
from app import db
from flask_sqlalchemy import SQLAlchemy

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    #set videos_checked_out_count equal to len(videos)??
    videos_checked_out_count = db.Column(db.Integer)
    rentals = db.relationship("Rental", backref="rentals", lazy=True)
    __tablename__ = "customers"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "postal_code": self.postal_code,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }