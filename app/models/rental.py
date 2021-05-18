from app import db
from app.models.video import Video
from app.models.customer import Customer


class Rental(db.Model):
    
    customer_id=db.Column(db.Integer,db.ForeignKey('customer.id'),primary_key=True)
    video_id=db.Column(db.Integer,db.ForeignKey('video.id',primary_key=True))
    
    results=db.session.query(Customer,Video,Rental).join(Customer,Customer.id == Rental.customer_id)\
            .join(Video,Video.id==Rental.video_id).filter(Customer.id==X).all() 

#need to generate a due date, 7 days from release date
