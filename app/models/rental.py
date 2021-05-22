from flask import current_app, make_response
from app import db
from sqlalchemy.orm import relationship
from datetime import timedelta
from datetime import datetime
from .customer import Customer
from .video import Video

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    video_id = db.Column(db.Integer, db.ForeignKey("video.video_id")) #do we need primary key?
    due_date = db.Column(db.DateTime)
    customer = db.relationship('Customer', backref='rentals', lazy=True)
    video = db.relationship('Video', backref='rentals', lazy=True)

    
    @classmethod
    def checkout(cls, customer_id, video_id):
 
        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)


        due_date = datetime.now() + timedelta(days=7)
        new_rental = Rental(
    
                customer_id = customer.customer_id,
                video_id = video.video_id,
                due_date = due_date
    )
 

        # video.inventory_checkout()
        # customer.added_checkout()
        video.available_inventory -= 1
        customer.videos_checked_out_count += 1

        db.session.add(new_rental)
        db.session.commit()

        return new_rental

    @classmethod
    def checkin(cls, customer_id, video_id):
        #rental = Rental.query.filter_by(customer_id, video_id)
        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)
        if customer.videos_checked_out_count == 0:
            return make_response({"details": "invalid data"}, 400)

        customer.videos_checked_out_count -= 1
        video.available_inventory += 1

        db.session.add(customer)
        db.session.add(video)
        #db.session.delete(rental)
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
