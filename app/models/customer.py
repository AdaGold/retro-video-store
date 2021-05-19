from flask import current_app
from app import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out_count = db.Column(db.Integer, default=0)

    def to_json(self):
        return  {
        "id": self.id,
        "name": self.name,
        "postal_code": self.postal_code,
        "phone": self.phone,
        "registered_at": self.registered_at,
        "videos_checked_out_count": self.videos_checked_out_count
        }
        

