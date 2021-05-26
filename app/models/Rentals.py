from app import db
from flask import current_app, make_response
from sqlalchemy import DateTime
from app.models.customer import Customer
from app.models.video import Video
from datetime import date, datetime, timedelta

class Rental(db.Model):
    __tablename__ = "rentals"
    rental_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"))
    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"))
    check_out_date = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime, default= ((datetime.now())+timedelta(days=7)))
    
    def rental_info(self):
        customer = Customer.query.get(self.customer_id)
        video = Video.query.get(self.video_id)
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": customer.videos_checked_out_count, #customer not and attribbute
            "available_inventory": video.available_inventory
        }
  

        

