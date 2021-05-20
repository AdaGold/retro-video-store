from flask import current_app
from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    register_at = db.Column(db.DateTime, nullable = True)
    videos_checked_out_count = db.Column(db.Integer, default=0)

    def json_response(self):
        response = {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "register_at": self.register_at,
            "videos_checked_out_count": self.videos_checked_out_count
            }

        return response