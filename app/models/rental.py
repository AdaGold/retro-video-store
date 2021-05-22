from app import db
from app.models.video import Video
from app.models.customer import Customer
from sqlalchemy.orm import relationship, backref
from datetime import timedelta, datetime


class Rental(db.Model):
    
    customer_id=db.Column(db.Integer,db.ForeignKey('customer.id'),primary_key=True)
    video_id=db.Column(db.Integer,db.ForeignKey('video.id'),primary_key=True)
    
    
    due_date= db.Column(db.DateTime(), nullable=True, default=(datetime.today() + timedelta(days=7)))
    
    customer = relationship(Customer,backref=backref("rental",cascade=None))
    video = relationship(Video,backref=backref("rental",cascade=None))
    
   

    
    def rental_check_out(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": self.due_date,
            "videos_checked_out_count": self.customer.videos_checked_out_count(),#increment by one
            "available_inventory": self.video.available_inventory() #decrease this one
        }
      

    def rental_check_in(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": self.customer.videos_checked_out_count(),#decrease by one
            "available_inventory": self.video.check_in_inventory() #increase by one

        }

    def get_rentals_by_video(self):
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