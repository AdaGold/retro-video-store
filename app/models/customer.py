from flask import current_app
from app import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "postal_code": self.postal_code,
            "register_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }