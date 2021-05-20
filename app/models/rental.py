from flask import current_app
from app import db
from datetime import date, timedelta
from .customer import Customer
from .video import Video

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.Date)
    
    def get_rentals(self):
        checked_out = db.session.query(Customer, Video, Rental)\
            .join(Customer, Customer.id==Rental.customer_id)\
                .join(Video, Video.id==Rental.video_id)\
                    .filter(Customer.id==self.customer_id)
        return len([vid for vid in checked_out])
    
    def get_customer(self):
        customers = db.session.query(Customer, Video, Rental)\
            .join(Customer, Customer.id==Rental.customer_id)\
                .join(Video, Video.id==Rental.video_id)\
                    .filter(Video.id==self.video_id)
        return [customer for customer in customers]
    

    def build_dict(self):

        return {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "due_date" : date.today() + timedelta(7),
            "videos_checked_out_count" : self.get_rentals(),
            "available_inventory" : len(self.get_customer())
            }