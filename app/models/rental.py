from flask import current_app
from flask.wrappers import Response
from app import db
import datetime
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, make_response
from datetime import timedelta
from sqlalchemy.orm import relationship


class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id')) # Foriegn key from customer class
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))# foriegn key from video class
    due_date = db.Column(db.DateTime)

    # foriegn keys relationships only coming from customer and video class
    customer = relationship("Customer", back_populates="rentals")
    video = relationship("Video", back_populates="rentals")

    
    def display_json(self):
        return {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "due_date" : self.due_date
        }


# CHECK IF WE HAVE A VIDEO AVAILABLE FOR RENTAL +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Rental_handler():

    @classmethod
    def check_out(cls, data):
        video = Video.query.get(data["video_id"])
        
        rentals = Rental.query.filter_by(video_id = video.video_id).count()

        if rentals < video.available_inventory:
            return make_response({"details": "Video out of stock"},400)

        new_rental = Rental(
            customer_id = data["customer.customer_id"],
            video = data["video.video_id"],
            due_date = datetime.datetime.now() + timedelta(days=7)
        )

        db.session.add(new_rental)
        db.commit()

        return make_response(new_rental),200


        