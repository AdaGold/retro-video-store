from flask import current_app
from app import db
from sqlalchemy.orm import relationship, backref


class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    videos_checked_out = db.Column(db.Integer, default=0)

    videos = relationship("Video", secondary="rental", backref=db.backref("customers"), lazy=True)

    def to_json_customer(self):
        return {
            "id": self.id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone_number,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_checked_out
        }