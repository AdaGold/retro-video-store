from flask import current_app
from app import db
from datetime import datetime 

class Rental():
    rental_id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime, nullable=False)
    #form one to many relation ----> customer and rental
    #form one to many relation ----> Video and rental

    def checkout_video(self):
            return {
                "customer_id": "",
                "video_id": "",
                "due_date": "",
                "videos_checked_out_count": "",
                "available_inventory": ""
            }, 200

    def check_in_video(self):
            return {
                "customer_id": "",
                "video_id": "",
                "videos_checked_out_count": "",
                "available_inventory": ""
            }, 200