from flask import current_app
from app import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Customer(db.Model):
    __tablename__= "customer"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime, nullable = True)
    videos_checked_out_count = db.Column(db.Integer, server_default=db.text("0"))
    video = relationship("Rental", back_populates = "customer")

    def to_json(self):
        customer = {
            "id": self.id,
            "name": self.name,
            "postal_code": int(self.postal_code),
            "phone": self.phone,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.current_videos()
        }

        return customer

    def to_json_with_id(self):
        return {
            "id": self.id
        }

    def is_int(self):
        try:
            return int(self.id)
        except ValueError:
            return False

    def current_videos(self):
        return len(self.video)

