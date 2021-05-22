from flask import current_app
from sqlalchemy.orm import relationship
from app import db
from app.models.video import Video

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime(), nullable=True)
    videos_checked_out_count = db.Column(db.Integer, default=0)
    rentals = db.relationship("Rental", back_populates="customer")
    



    def to_json(self):

        regular_response = {

            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            "videos_checked_out_count": self.videos_checked_out_count
        }
        return regular_response
