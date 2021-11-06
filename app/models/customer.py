# from flask import current_app
from app import db
from sqlalchemy.schema import FetchedValue

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)


    def to_dict(self):
        return {
                "name": self.name,
                "id": self.id,
                "phone": self.phone,
                "postal_code": str(self.postal_code)
                }


