from flask import current_app
from app import db
from sqlalchemy.orm import relationship
from datetime import timedelta
from datetime import datetime

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    video_id = db.Column(db.Integer, db.ForeignKey("video.video_id")) #do we need primary key?
    due_date = db.Column(db.DateTime)
    customer = db.relationship('Customer', backref='rentals', lazy=True)
    video = db.relationship('Video', backref='rentals', lazy=True)

    
    @classmethod
    def checkout(cls, customer_id, video_id):

        from .customer import Customer
        from .video import Video
 
        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)
        # if video.available_inventory < 1:
        #     return False

        due_date = datetime.now() + timedelta(days=7)
        new_rental = Rental(
    
                customer_id = customer.customer_id,
                video_id = video.video_id,
                due_date = due_date
    )
        db.session.add(new_rental)
        db.session.commit()

        video.inventory_checkout()
        customer.added_checkout()

        return new_rental

    @classmethod
    def checkin(cls, customer_id, video_id):

        from .customer import Customer
        from .video import Video
 
        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)
        
        customer.decrease_checkout()
        video.inventory_checkin()

        
        db.session.commit()

        return {
            "customer_id": customer_id,
            "video_id": video_id,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.available_inventory
        }

    
    def customer_id_rentals(self):
        
        return {
            "release_date": self.video.release_date,
            "title": self.video.title,
            "due_date": self.video.due_date
        }

    def return_rental_info(self):
        return {"customer_id" : self.customer_id,
                "video_id" : self.video_id,
                "due_date" : self.due_date,
                "videos_checked_out_count": self.customer.videos_checked_out_count,
                "available_inventory": self.video.available_inventory
        }
