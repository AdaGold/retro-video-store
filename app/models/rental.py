#WAVE 2
from flask import current_app
from app import db
from app.models.customer import Customer #wave 2
from app.models.video import Video #wave 2
from datetime import datetime, timedelta


class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime, nullable = False)
    #form one to many relation between customer and rental
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    #form one to many relation between Video and rental
    video_id  = db.Column(db.Integer, db.ForeignKey('video.video_id'))
    
    
    def checkout_detail(self):
        return {
                    "customer_id": self.customer_id,
                    "video_id": self.video_id,
                    "due_date": self.due_date,
                    #"videos_checked_out_count": self.calc_videos_checked_out(),
                    #"available_inventory": self.calculate_available_inventory()
                }
    
      # def create_due_date(self):
    #     days = timedelta(days=7)
    #     self.due_date = datetime.now() + days
    #     return self.due_date
    
    # def calculate_available_inventory(self):
    #     self.available_inventory = Video.total_inventory - len(Video.rentals)
    #     return self.available_inventory
    
    # def calc_videos_checked_out(self):
    #     result = len(Customer.rentals)
    #     return result
  