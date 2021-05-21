import datetime
from flask import current_app
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta


class Rental(db.Model):
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    # should set the server_default instead of at route for best practice
    due_date = db.Column(db.DateTime) 
    video = db.relationship("Video", back_populates="customers")
    customer = db.relationship("Customer", back_populates="videos")