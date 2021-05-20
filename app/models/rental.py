from flask import current_app
from app import db
from datetime import datetime, timedelta


class Rental(db.Model):
    __tablename__ = 'rentals'
    rental_id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey('customers.customer_id'))

    video_id = db.Column(
        db.Integer,
        db.ForeignKey('videos.video_id'))

    due_date = db.Column(
        db.DateTime,
        default=(datetime.today() + timedelta(days=4)).strftime("%Y-%m-%d")
    )

    def to_json(self):
        """Converts a Rental instance into JSON"""
        response_body = {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date
        }
        return response_body
