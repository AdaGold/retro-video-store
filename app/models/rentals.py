# from app.models.customers import Customer
from flask import current_app
from sqlalchemy.orm import defaultload
# from app.models.videos import Video
from app import db
from datetime import datetime

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.customer_id'),nullable=True) 
    video_id = db.Column(db.Integer,db.ForeignKey('video.video_id'),nullable=True) 
    due_date = db.Column(db.DateTime,nullable=True)
    
    
    def rental_to_json(self):
        return {
            "customer_id":self.customer_id,
            "video_id":self.video_id,
            "due_date":self.due_date,
            # "videos_checked_out_count":customer.videos_checked_out_count,
            # "available_inventory":video.available_inventory

        }

    
        