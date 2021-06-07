from flask.globals import current_app
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime, timedelta
from flask import current_app
from app import db 

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"), primary_key = True)
    video_id = db.Column(db.Integer, db.ForeignKey("videos.video_id"), primary_key = True)
    due_date = db.Column(db.DateTime, default=(datetime.now() + timedelta(7)))

    def rental_ops(self):
        rental_dict = {
            "customer_id":self.customer_id,
            "video_id:":self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": Customer.query.get(self.customer_id).videos_checked_out_count,
            "available_inventory": Video.query.get(self.video_id).available_inventory
        }
        return rental_dict








