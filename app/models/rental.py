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
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'))
    video_id = db.Column(db.Integer,db.ForeignKey('video.id'))
    due_date = db.Column(db.DateTime)

   
    @classmethod#built in python method that allows you to pass a class as an argument, rather than an instance
    def checkout(cls,customer_id,video_id): 
        """
            Input:  customer_id, video_id
            Output: new instance of Rental with customer_id, video_id, due_date
        """
        from .customer import Customer#gets access to Customer Class
        from .video import Video#gets access to Video Class
        customer = Customer.query.get(customer_id)#querying Customer using customer_id
        video = Video.query.get(video_id)#querying Video for video_id
        due_date = datetime.datetime.now() + datetime.timedelta(days=7)
        new_rental = Rental(
                    customer_id = customer.id,
                    video_id = video.id,
                    due_date = due_date 
                    )
        db.session.add(new_rental)
        db.session.commit()
        customer.increase_checkout_count()#calling Customer instance helper function on instance of Customer
        video.decrease_inventory()#calling Video helper function on instance of Video
        return new_rental
    
   
    def to_python_dict(self):
        """
            Input:  instance of Rental 
            Ouput:  python dictionary of Rental instance with added keys customer.videos_checked_out_count and 
                    video.available_inventory
        """
        from .customer import Customer#gives access to Customer model
        from .video import Video#gives access to Video model
        
        customer = Customer.query.get(self.customer_id)# taking from self
        video = Video.query.get(self.video_id)
        
        return {
                
                "customer_id": self.customer_id,
                "video_id": self.video_id,
                "due_date": str(self.due_date),
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory
            }
    
    # @classmethod
    # def check_in(cls,customer_id,video_id):
    #     """
    #         Input:  customer_id, video_id
    #         Output: new instance of Rental with customer_id, video_id, due_date
    #     """
    #     from .customer import Customer
    #     from .video import Video
    #     customer = Customer.query.get(customer_id)#querying Customer using customer_id
    #     video = Video.query.get(video_id)
    #     updated_videos = Rental
        
        
     
        
        
        # results = db.session.query(Customer, Video, Rental).join(Customer, Customer.id==Rental.customer_id)\
        #     .join(Video, Video.id==Rental.video_id).filter(Customer.id == customer_id).all()#customer id is final filter for the tuples. we are designating Customer.id == customer_id meaning results variable will containa tuple list of all movies checked out by customer id. contains(customer, video, rental)
        #     #iterate thorugh list of tuples  for custome, video, rental in results
        
        # for customer, video, rental in results:# looping through list of tuples to find the movie that customer just checked in to delete it from the db
        #     if video.id == video_id:
        #         db.session.delete(rental)
        #         db.session.commit()
        #         return