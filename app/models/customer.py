from flask import current_app
from app import db
# from datetime import datetime
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Table, Column, Integer, ForeignKey 

# from flask_migrate import Migrate


class Customer(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String)    
    register_at = db.Column(db.DateTime, nullable=True) # nullable=True ??? 
    postal_code = db.Column(db.String) 
    phone = db.Column(db.String) 

    # videos_chekced_out_count =  db.Column(db.Integer, db.ForeignKey("video.video_id"), nullable=True)
    videos_checked_out_count =  db.Column(db.Integer, default=0)
    
    # videos = db.relationship("Rental", backref="customers", lazy=True)
    


    def get_json(self):
        return {
            "id":self.customer_id,
            "name":self.name,
            "registered_at":self.register_at,
            "postal_code":int(self.postal_code),
            "phone":self.phone,
            "videos_checked_out_count":self.videos_checked_out_count
            }
            