from sqlalchemy.orm import relationship, backref
from app.models import customer
from app.models import video 
from flask import current_app
from app import db

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=True)
    due_date = db.Column(db.DateTime, nullable = True)

    customer = relationship('Customer', backref = 'rentals')
    video = relationship('Video', backref = 'rentals')


    def to_json_rental(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date, #7 days from checked out date
            "videos_checked_out_count": self.customer.checkout_count,
            "available_inventory": self.video.available_inventory 
        }


