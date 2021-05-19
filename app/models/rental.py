from flask import current_app
from app import db

class Rental(db.Model):
    video_id = db.Column(db.Integer, db.ForeignKey('video.video.id'), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer.id'), primary_key=True)