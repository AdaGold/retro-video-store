from flask import current_app
from app import db
# from app.models.customer import Customer
# from app.models.video import Video
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rental(Base):
    __tablename__ = 'rental'
    #source i got from didnt have db.Column, just Column, integret and foreignkey.  Why?  is it because i dont have rental_id?
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    video = relationship("Video", back_populates="renters")
    customer = relationship("Customer", back_populates="rentals")
    due_date = db.Column(db.DateTime)


    # def api_response(self, customer): 
    #     response_body = {
    #                     "customer_id": self.customer_id,
    #                     "video_id": self.video_id,
    #                     "due_date": self.due_date,
    #                     "total_inventory": self.total_inventory,
    #                     "videos_checked_out_count": customer.videos_checked_out_count,
    #                     "available_inventory": 0
    #                     # "available_inventory": calc_available_inventory()
    #                     }

    #     return response_body
