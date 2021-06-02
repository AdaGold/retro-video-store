from flask import current_app
from app import db
from sqlalchemy.orm import relationship


class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    video = relationship("Rental", back_populates="customer")

    def to_json(self):
        customer_dict = {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone_number,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out_count
        }
        return customer_dict