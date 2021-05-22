from flask import current_app
from app import db 
from datetime import datetime, timedelta

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime,default= datetime.now()+timedelta(days=7))
    videos_checked_out_count = db.Column(db.Integer, default=0)
    rentals = db.relationship("Rental", back_populates="customer", lazy=True)

    def customer_to_json(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "registered_at" : self.registered_at,
            "postal_code" : self.postal_code,
            "phone" : self.phone,
            "videos_checked_out_count" : self.videos_checked_out_count}
