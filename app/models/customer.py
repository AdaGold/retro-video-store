from flask import current_app
from app import db
from datetime import datetime

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name =  db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, default=datetime.utcnow())
    videos_checked_out_count = db.Column(db.Integer, nullable =True)

    def to_json(self):
        if self.videos_checked_out_count:
            return{
                "id": self.customer_id,
                "name": self.name,
                "phone": self.phone,
                "postal_code": self.postal_code,
                "registered_at": self.register_at,
                "videos_checked_out_count": self.videos_checked_out_count
            }
        else:
            return{
                "id": self.customer_id,
                "name": self.name,
                "phone": self.phone,
                "postal_code": self.postal_code,
                "registered_at": self.register_at,
                "videos_checked_out_count": 0
            }