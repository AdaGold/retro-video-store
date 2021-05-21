from flask import current_app
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone_number = db.Column(db.String)
    register_at = db.Column(db.DateTime, nullable = False)
    videos_checked_out = db.Column(db.Integer, default=0)
    videos = db.relationship("Rental", back_populates="customer")


    def make_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "registered_at": self.register_at,
            "postal_code": str(self.postal_code),
            "phone": self.phone_number,
            "videos_checked_out_count": self.videos_checked_out
        }
    def return_id(self):
        return {"id":self.id}

    def check_out(self):
        self.videos_checked_out += 1

    def check_in(self):
        self.videos_checked_out -= 1
        