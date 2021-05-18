from flask import current_app
from app import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out_count = db.Column(db.Integer)

def to_json(self):
    return {
        "id": self.id,
        "name": self.name,
        "postal code": self.postal_code,
        "phone": self.phone,
        "registered at": self.registered_at,
        "videos_checked_out_count": self.videos_checked_out_count
    }

def to_json_with_id(self):
    return {
        "id": self.id
    }