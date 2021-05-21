from flask import current_app
from app import db
from datetime import datetime, timedelta 
from sqlalchemy.orm import relationship

class Rental(db.Model):
    __tablename__= "rental"
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.Integer, nullable=True, default = datetime.now() + timedelta(days=7))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video = relationship("Video", back_populates = "customer")
    customer = relationship("Customer", back_populates = "video")
    # create the one to many relationship ----> customer && rental
    # create the one to many relationship ----> Video && rental

    def is_int(self):
        try:
            return int(self.id)
        except ValueError:
            return False

    # def checkout_video(self):
    #         return {
    #             "customer_id": "",
    #             "video_id": "",
    #             "due_date": "",
    #             "videos_checked_out_count": "",
    #             "available_inventory": ""
    #         }, 200

    # def check_in_video(self):
    #         return {
    #             "customer_id": "",
    #             "video_id": "",
    #             "videos_checked_out_count": "",
    #             "available_inventory": ""
    #         }, 200