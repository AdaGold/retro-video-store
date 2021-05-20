from app.models.video import Video
from app.models.customer import Customer
from flask import current_app, make_response
from app import db
# from .customer import Customer
# from .video import Video
# from datetime import datetime, timedelta

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True)
    due_date = db.Column(db.DateTime, nullable = True)
    # customer = db.relationship("Video", back_populates="customers")    
    # video = db.relationship("Customer", back_populates="videos")    

    def make_json(self, customer_id, video_id):

        if self.due_date == None:
            return {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "videos_checked_out_count": self.get_checked_out_count(customer_id),
                "availibe_inventory": self.get_availible_inventory(video_id)
            }
        else:    
            return {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date,
                "videos_checked_out_count": self.get_checked_out_count(customer_id),
                "availibe_inventory": self.get_availible_inventory(video_id)
            }
    def get_checked_out_count(self, customer_id):
        customer = Customer.query.get(customer_id)
        return customer.videos_checked_out

    def get_availible_inventory(self, video_id):
        video = Video.query.get(video_id)
        return video.availible_inventory

    # try class method? for rental creation
    # def check_out(self, customer_id, video_id): 
    #     customer = Customer.query.get(customer_id)
    #     video = Video.query.get(video_id)

    #     if customer.check_out() == None:
    #         return make_response("Video not availible", 400)
        
    #     else:
    #         customer.check_out()
    #         video.check_out()

    #         new_rental= \
    #             self(due_date=(datetime.now() + timedelta(days=7)), \
    #                 customer_id=customer_id, video_id=video_id)

    #         db.session.add(new_rental)
    #         db.session.commit()
            
    #         return make_response(new_rental.make_json(customer_id, video_id))

    # def check_in(self, customer_id, video_id):
    #     customer = Customer.query.get(customer_id)
    #     video = Video.query.get(video_id)

    #     returned_rental = self(due_date=None, customer_id=customer_id, video_id=video_id)
        
    #     customer.check_in()
    #     video.check_in()

    #     db.session.add(returned_rental)
    #     db.session.commit()
        
    #     return make_response(returned_rental.make_json(customer_id, video_id))