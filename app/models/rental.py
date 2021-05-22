from flask import current_app
from app import db
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime, timedelta

class Rental(db.Model):
    # rental_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True)
    due_date = db.Column(db.DateTime, default = datetime.now() + timedelta(days=7))
    # , nullable = True, default = datetime.now() + timedelta(days=7))
    customer = db.relationship("Customer", backref="rental",lazy=True)
    video = db.relationship("Video", backref="rental",lazy=True)