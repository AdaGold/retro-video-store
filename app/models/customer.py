from flask import current_app
from app import db
from datetime import datetime


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer, server_default=db.text("0"))

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }

    def to_json_with_id(self):
        return {
            "id": self.id
        }


    def is_int(self):
        try:
            return int(self.id)
        except ValueError:
            return False