from flask import current_app
from app import db
from datetime import timedelta, datetime

# association table 
class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id')) #foreign coming from customer model 
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id')) #foreign coming from video model 
    due_date = db.Column(db.DateTime, nullable = True, default = datetime.now() + timedelta(days=7)) 
    # create a due date. The rental's due date is the seven days from the current date

    def to_json_rental(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": self.videos_checked_out_count,# this comes from customer model 
            "available_inventory": self.available_inventory # this comes from video model 
        }
