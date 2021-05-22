
from sqlalchemy.orm import relationship
from app.models.video import Video
from app.models.customer import Customer
from flask import current_app
from app import db
from datetime import timedelta, datetime
# import datetime
from flask import make_response


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'))
    due_date = db.Column(db.DateTime)

    video = relationship("Video", back_populates="rentals")
    customer = relationship("Customer", back_populates="rentals")
    
    
    @classmethod
    def check_out(cls, customer_id, video_id):

        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)

        rental= cls(customer_id = customer_id,
                            video_id = video_id,
                            due_date = datetime.today() + timedelta(days=7))
        
        if video.available_inventory < 0:
            return make_response({"details": "Video out of stock"}, 400)

        video.available_inventory -= 1
        customer.videos_checked_out_count += 1
        
        db.session.add(rental)
        db.session.commit()

        return rental

    def to_json(self):
        regular_response = {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date.isoformat(),
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
        }
        return regular_response

    @classmethod
    def check_in(cls, customer_id, video_id):

        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)
        rentals = Rental.query.filter(Rental.video_id==video_id).all()
        for rental in rentals:
            if rental.customer_id == customer_id:

                video.available_inventory += 1
                customer.videos_checked_out_count -= 1

                db.session.delete(rental)
                db.session.commit()

                return rental
        
        return None


    def to_dict(self):

        regular_response = {
            "customer_id" : self.customer_id,
            "video_id" : self.video_id,
            "videos_checked_out_count": self.customer.videos_checked_out_count,
            "available_inventory": self.video.available_inventory
        }
        return regular_response

