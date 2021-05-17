from flask import current_app
from app import db
# from sqlalchemy.orm import relationship

class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone_number = db.Column(db.String)
    register_at = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer)

    def to_json(self):
        customer_json = {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone_numder": self.phone_number,
            "register_at": self.register_at
        }
        return customer_json

