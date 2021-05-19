from flask import current_app
from app import db
from datetime import datetime 


class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime, nullable=False)
    #form one to many relation between customer and rental
    #form one to many relation between Video and rental
    
    
    def checkout_detail(self):
        return {
                    #"customer_id": 122581016,
                    #"video_id": 235040983,
                    "due_date": self.due_date
                    #"videos_checked_out_count": 2,
                    #"available_inventory": 5
                }
        
    def checkin_detail(self):
        return {
                    #"customer_id": 122581016,
                    #"video_id": 277419103,
                    #"videos_checked_out_count": 1,
                    #"available_inventory": 6
                }