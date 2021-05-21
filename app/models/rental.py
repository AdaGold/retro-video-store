from flask import current_app
from app import db
from datetime import date, timedelta
from .customer import Customer
from .video import Video

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    due_date = db.Column(db.Date(), default = date.today() + timedelta(7), nullable=True)

    def build_dict(self):
        #builds primary rental dictionary
        video = Video.query.get(self.video_id)
        customer = Customer.query.get(self.customer_id)
        rental = {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "videos_checked_out_count" : customer.count_videos(),
            "available_inventory" : video.calculate_inventory()
            }
        if self.due_date:
            rental["due_date"] = self.due_date
        return rental
    
    def customers_dict(self):
        #builds dictionary for customer rentals
        customer = Customer.query.get(self.customer_id)

        return {
            "name" : customer.name,
            "phone" : customer.phone,
            "postal_code" : customer.postal_code,
            "due_date" : self.due_date


        }
    
    def rentals_by_cust(self):
        #builds dictionary for videos by customer
        video = Video.query.get(self.video_id)

        return {
            "title" : video.title,
            "release_date" : video.release_date,
            "due_date" : self.due_date
        } 
    
    def check_in_dict(self):
        #builds dictionary for check in
        video = Video.query.get(self.video_id)
        customer = Customer.query.get(self.customer_id)

        return {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "videos_checked_out_count" : customer.count_videos(),
            "available_inventory" : video.calculate_inventory()
        }
    def check_out_dict(self):
        video = Video.query.get(self.video_id)
        customer = Customer.query.get(self.customer_id)

        return {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "videos_checked_out_count" : customer.count_videos(),
            "available_inventory" : video.calculate_inventory(), 
            "due_date" : self.due_date
        }
    