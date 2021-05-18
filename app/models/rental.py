from flask import current_app
from app import db
import datetime 

class Rental(db.Model):
    """
    Attributes:
        id
        customer_id
        video_id
        due_date
    """

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'),primary_key=True)
    video_id = db.Column(db.Integer,db.ForeignKey('video.id'),primary_key=True)
    due_date = db.Column(db.DateTime)

   

    @classmethod#built in python method that makes a method universal
    def checkout(cls,customer_id,video_id): 
        """
            Input: class name, customer_id,video_id
            Output: new instance of Rental with customer_id, video_id, due_date
        """
        from .customer import Customer#gets access to Customer Class
        from .video import Video#gets access to Video Class
        customer = Customer.query.get(customer_id)#querying Customer by customer_id
        video = Video.query.get(video_id)#querying Video for video_id
        due_date = datetime.datetime.now() + datetime.timedelta(days=7)
        new_rental = Rental(
                    customer_id = customer.id,
                    video_id = video.id,
                    due_date = due_date 
                    )
        db.session.add(new_rental)
        db.session.commit()
        return new_rental
    
    
    def to_python_dict(self):
        """
            Input:

        """
        
        return {
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": self.due_date.strftime(format)#
                
            

        }