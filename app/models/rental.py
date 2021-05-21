from flask import current_app
from app import db
from datetime import datetime, timedelta
from app.models.customer import Customer
from app.models.video import Video

class Rental(db.Model): 
    rental_id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime, nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"), nullable=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.video_id"), nullable=True)

    def check_out_to_json(self, customer, video): 
        to_json = {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date,
                "videos_checked_out_count": customer.videos_checked_out_count, 
                "available_inventory": video.available_inventory            
        }
        return to_json

    def customers_associated_rentals(self, video): 
        return {
                "release_date": video.release_date, 
                "title": video.title, 
                "due_date": self.due_date
        }
    
    def videos_associated_rentals(self, customer): 
        return {
                "name": customer.name, 
                "phone": customer.phone, 
                "postal_code": customer.postal_code,
                "due_date": self.due_date
        }

    @classmethod
    def make_a_rental(cls, json, id): 
        return cls(rental_id=id,
                    due_date=datetime.utcnow()+timedelta(days=7),
                    customer_id=json["customer_id"], 
                    video_id=json["video_id"])