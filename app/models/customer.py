from flask import current_app
from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String)
    registered_at = db.Column(db.DateTime)

    # __tablename__ = "customer_id"
    videos_checked_out = db.Column(db.Integer)
     

    def to_json_customer(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone_number,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out
        }

    # def to_json_customer(self):
    #     return {
    #         "id": self.customer_id,
    #         "name": self.name,
    #         "registered_at": self.registered_at,
    #         "postal_code": self.postal_code,
    #         "phone": self.phone_number,
    #         "videos_checked_out_count": self.videos_checked_out            
    #     }