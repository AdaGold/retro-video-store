from app import db
from flask import current_app
from sqlalchemy import DateTime


class Rental(db.Model):
    __tablename__ = "Rental"
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customer.customer.id"), primary_key=True)
    video_id = db.Column(
        db.Integer, db.ForeignKey("video.video.id"), primary_key=True)
    video = db.relationship("Video", back_populates="customers")
    customer = db.relationship("Customer", back_populates="videos")

    # DUE_DATE
    due_date = db.Column(db.DateTime, default=)

    # def helper():
