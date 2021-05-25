from flask import current_app
from app import db


class Customer(db.Model):
    __tablename__ = 'customers'
    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    registered_at = db.Column(db.DateTime, nullable=True)
    postal_code = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String, nullable=False)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    rented = db.relationship("Rental", back_populates="customer_rentals")


    def customers_json_format(self):
        return {
            "id": self.client_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count
            }
