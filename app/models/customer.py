from flask import current_app
from app import db
from sqlalchemy import DateTime
from app.models.rental import Rental


class Customer(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable=True)
    videos = db.relationship("Video", secondary="rentals", back_populates="customers")

    def to_json(self):
        customer = {
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.register_at,
            "phone": self.phone,
            "postal_code": self.postal_code,
            "videos_checked_out_count": self.get_checked_out()
        }

        return customer

    def get_checked_out(self):
        return len(self.videos)