from flask import current_app
from app import db
from datetime import datetime, timedelta


class Rental(db.Model):
    __tablename__ = 'rentals'
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vhs_id = db.Column(db.Integer, db.ForeignKey('videos.video_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.client_id'))
    due_date = db.Column(db.DateTime, default=datetime.now)
    customer_rentals = db.relationship("Customer", back_populates="rented")
    videos_rented = db.relationship("Video", back_populates="videos_for_rent")


    def rental_to_json_format(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.vhs_id,
            "videos_checked_out_count": self.customer_rentals.videos_checked_out_count,
            "due_date": self.due_date,
            "available_inventory": self.videos_rented.available_inventory
            }


    def check_in_json_format(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.vhs_id,
            "videos_checked_out_count": self.customer_rentals.videos_checked_out_count,
            "available_inventory": self.videos_rented.available_inventory
            }


    def get_customer_rental_json(self):
        return {
            "release_date": self.videos_rented.release_date,
            "title": self.videos_rented.title,
            "due_date": self.due_date
        }


    def get_video_rental_json(self):
        return {
            "name": self.customer_rentals.name,
            "phone": self.customer_rentals.phone,
            "due_date": self.due_date,
            "postal_code": self.customer_rentals.postal_code
        }