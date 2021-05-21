from flask import current_app
from sqlalchemy.orm import relationship
from app import db


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime)
    check_in_date = db.Column(db.DateTime, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))

    customer = relationship('Customer', back_populates='rentals')
    video = relationship('Video', back_populates='rentals')


    def to_json_customer(self):
        return {
            "id": self.id,
            "release_date": self.video.release_date,
            "title": self.video.title,
            "due_date": self.due_date
        }

    def to_json_video(self):
        return {
            "due_date": self.due_date,
            "name": self.customer.name,
            "phone": self.customer.phone,
            "postal_code": self.customer.postal_code,
        }
