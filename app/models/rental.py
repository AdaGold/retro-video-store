from flask import current_app
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Rental(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"))
    due_date = db.Column(db.DateTime, nullable = False) 