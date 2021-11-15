from sqlalchemy.orm import backref
from app import db
from datetime import datetime, timedelta

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), primary_key=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean, default = False)
    #customer = db.relationship("Customer", backref='rentals', lazy=True)
    #video = db.relationship("Video", backref='rentals', lazy=True)