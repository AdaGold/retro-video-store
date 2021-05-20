from datetime import datetime
from flask import current_app
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime


class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    registered_at = db.Column(
        db.DateTime,
        default=datetime.now())
    # videos = relationship("Rental", back_populates="customer")

    def to_json(self):
        """Converts a Customer instance into JSON"""
        response_body = {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }
        return response_body

    def from_json(self, json):
        """Converts JSON into a new instance of Customer"""
        self.name = json["name"]
        self.postal_code = json["postal_code"]
        self.phone = json["phone"]
        # self.registered_at = json["registered_at"]
        return self

    # def is_phone_valid():
    #     """Validates the phone number to follow the pattern XXX-XXX-XXXX""
    #     pass
