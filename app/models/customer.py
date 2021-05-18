from flask import current_app
from app import db
# from sqlalchemy.orm import relationship

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)



    def to_json(self):
        if not self.videos_checked_out_count:
            self.videos_checked_out_count = 0
        customer_json = {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }
        return customer_json

