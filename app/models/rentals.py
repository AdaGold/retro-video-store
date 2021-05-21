from app.models import customer
from flask import current_app # faded font color suggests unnecessary
from app import db
from datetime import timedelta, datetime 
#from app.models import Customer

class Rental(db.Model): # represents the taking of the video from blockbuster
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column('customer_id', db.Integer, db.ForeignKey('customer.customer_id'))
    video_id = db.Column('video_id', db.Integer, db.ForeignKey('video.video_id'))
    check_out_date = db.Column('check_out_date', db.DateTime, default=datetime.now()) # leave default off bc taken care of in route

    # says when i have rental and want the renter instance attached to it, i can access easily, via Rental.renter
    renter = db.relationship('Customer', backref='rentals', lazy=True, foreign_keys=customer_id) # backref properties need to change!! (maybe); was 'renter =...'
    video = db.relationship('Video', backref='rentals', lazy=True, foreign_keys=video_id)

    def to_json(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.check_out_date + (timedelta(days=7)),
            "videos_checked_out_count": self.renter.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
            }
