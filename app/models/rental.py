from flask import current_app
from app import db
from app.models.customer import Customer
from app.models.video import Video
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

class Rental(db.Model):
    #source i got from didnt have db.Column, just Column, integret and foreignkey.  Why?  is it because i dont have rental_id?
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    #should i "" Video and Customer?
    # Customer = relationship("Customer", backref=backref("rentals"))
    video = relationship("Video", backref="renters")
    customer = relationship("Customer", backref="rentals")
    due_date = db.Column(db.DateTime)

