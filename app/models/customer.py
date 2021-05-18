from flask import current_app
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone_number = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable = False)

    def make_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.register_at,
            "postal_code": self.postal_code,
            "phone": self.phone_number,
            "videos_check_out_count": 0
        }