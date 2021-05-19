from flask import current_app
from app import db

class Rental(db.Model):
    #rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.customer_id'), primary_key=True)
    due_date = db.Column(db.DateTime)