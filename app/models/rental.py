from app import db
from app.models.video import Video
from app.models.customer import Customer
from sqlalchemy.orm import relationship, backref
from datetime import timedelta, datetime


class Rental(db.Model):
    #id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    #composite Primary Key, in order to pass the tuple customer and video id, hence using them as primary keys
    customer_id=db.Column(db.Integer,db.ForeignKey('customer.id'),primary_key=True)
    video_id=db.Column(db.Integer,db.ForeignKey('video.id'),primary_key=True)
    
    #datetime.today()
    #default=(datetime.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    due_date= db.Column(db.DateTime(), nullable=True, default=(datetime.today() + timedelta(days=7)))
    # available_inventory=db.Column(db.Integer,default=Video.total_inventory)
    # videos_checked_out_count=db.Column(db.Integer,default=0)
    customer = relationship(Customer,backref=backref("rental",cascade=None))
    video = relationship(Video,backref=backref("rental",cascade=None))
    # results=db.session.query(Customer,Video,Rental).join(Customer,Customer.id == Rental.customer_id)\
    #         .join(Video,Video.id==Rental.video_id).filter(Customer.id==X).all() 
   

    
    def rental_check_out(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.customer.videos_checked_out_count(),#increment
            "available_inventory": self.video.available_inventory() #decrease this one
        }
        #     "videos_checked_out_count": self.find_number_of_checked_out_videos(),
        #     "available_inventory": self.find_available_inventory()
        # }

    def rental_check_in(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": self.customer.check_in_video_count(),#decrease by one
            "available_inventory": self.video.check_in_inventory() #increase by one

        }

    def get_customer_current_rentals(self):
        return {
            "due_date": self.due_date,
            "name": self.customer.name,
            "phone": self.customer.phone,
            "postal_code": self.customer.postal_code,
        }

    def get_rentals_by_customers(self):
        return {
            "due_date": self.due_date,
            "title": self.video.title,
            "release_date": self.video.release_date
            
        }