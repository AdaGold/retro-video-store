# from flask import current_app
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime)


    def to_dict(self):
        # is_complete = False if not self.completed_at else True
        return {
                "name": self.name,
                "id": self.id,
                "phone": self.phone,
                "postal_code": str(self.postal_code)
                }
