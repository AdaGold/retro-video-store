from flask import current_app
from app import db
from app.models.customer import Customer


class Video(db.Model):
    __tablename__="videos"

    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date_time = db.Column(db.DateTime, nullable=True) # correct?
    total_inventory = db.Column(db.Integer)
    # availiable_inventory = db.Column(db.Integer)
    
    customer_id = db.relationship("Customer",backref="video", lazy=True)