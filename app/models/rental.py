from app import db
from flask import current_app
from sqlalchemy import DateTime
from app.models.customer import Customer
from app.models.video import Video
# from sqlalchemy.orm import relationship, backref


class Rental(db.Model):
    __tablename__ = 'rentals'
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.customer_id"), primary_key=True)
    video_id = db.Column(
        db.Integer, db.ForeignKey("videos.video_id"), primary_key=True)

    # video = db.relationship('Video', back_populates='customers')
    # customer = db.relationship('Customer', back_populates='videos')

    # video = db.relationship(Video, backref=backref(
    #     "rental", cascade="all, delete-orphan"))
    # customer = db.relationship(Customer, backref=backref(
    #     "rental", cascade="all, delete-orphan"))

    due_date = db.Column(db.DateTime)
    # , default=)
    # def helper():
