from flask import current_app
from app import db


class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone_number = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    videos_checked_out = db.Column(db.Integer)

    videos = db.relationship("Video", secondary="rental", backref="customer", lazy=True)

    def videos_default(self):
        if self.videos_checked_out is None:
            return 0
        else:
            return self.videos_checked_out


    def to_json_customer(self):
        return {
            "id": self.customer_id,
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone_number,
            "registered_at": self.registered_at,
            "videos_checked_out_count": self.videos_default()
        }

    def error_msg(self):
        return {"errors": "error message"}

