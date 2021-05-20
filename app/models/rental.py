from flask import current_app
from app import db
# from app.models.customer import Customer
# from app.models.video import Video
#from sqlalchemy import backref

class Rental(db.Model):
    __tablename__ = 'rentals'
    id = db.Column(db.Integer, primary_key =True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"))
    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"))

    # customer = db.relationship(Customer, backref=backref("rentals", cascade="all, delete-orphan"))
    # video = db.relationship(Video, backref=backref("rentals", cascade="all, delete-orphan"))

