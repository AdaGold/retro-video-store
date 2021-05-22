from flask import current_app
from app import db
from datetime import datetime
from datetime import timedelta


# Establishing many-to-many relationships between Customer and Video 
# CustomerVideojoin Model (not Table)
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False) 
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False) # lazy?
    rental_date = db.Column(db.DateTime, default=datetime.utcnow(),  
        nullable=False) # maybe
    # due_date = # current date + 7 use delta
    due_date = db.Column(db.DateTime,  default = datetime.utcnow() + timedelta(days=7),
        nullable=False) #nullable = false?

    @staticmethod
    def from_json_to_check_out(request_body):
        '''
        Converts JSON request body into a new instance of Rental
        input: Takes in a dictionary in the shape of the JSON the API 
        receives. 
        output: instance of rental
        '''
        new_rental = Rental(customer_id=request_body["customer_id"],
                video_id=request_body["video_id"])
        return new_rental
    
    @staticmethod
    def customer_rentals_response(rental, video):
        '''
        Creates response with both Rental and Video instances
        input: Takes in a rental instance and a video instance  
        output: dictionary containing info of instances of video combined 
        with rental due date details
        '''
        return {"release_date": video.release_date.strftime("%Y-%m-%d"),
                "title": video.title,
                "due_date": rental.due_date.strftime("%a, %d %b %Y %X %z %Z")}

    @staticmethod
    def customer_due_date_response(rental, customer):
        '''
        Creates response with both Rental and Customer instances
        input: Takes in a rental and a customer instance  
        output: dictionary containing info of instances of rental combined 
        with customer details
        '''
        return {"due_date": rental.due_date.strftime("%a, %d %b %Y %X %z %Z"),
                "name": customer.name,
                "phone": customer.phone,
                "postal_code": str(customer.postal_code)}
