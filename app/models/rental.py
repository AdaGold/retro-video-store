from flask import current_app
from sqlalchemy.orm import relationship
from app import db


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))

    customer = relationship('Customer', back_populates='rentals')
    video = relationship('Video', back_populates='rentals')

