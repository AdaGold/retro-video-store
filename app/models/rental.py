from flask import current_app
from app import db
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta 



class Rental(db.Model):
    __tablename__= "rental"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.DateTime, nullable=True)
    video = relationship("Video", back_populates="customer")
    customer = relationship("Customer", back_populates="video")