from flask import current_app
from app import db
from datetime import datetime
from datetime import timedelta


# Establishing many-to-many relationships between Customer and Video 
# CustomerVideojoin Model/Table
class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) ##??
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False) # how about nullable= True or False?
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)# how about nullable= True or False?, do I add lazy?
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
    
    # def rental_to_json_response(self):
    #     '''
    #     Converts a Rental instance into JSON format
    #     Output: Returns a Python dictionary in the shape of JSON response 
    #     that the API returns in the route that is called (GET route).
    #     '''
    #     return  {"release_date": self.release_date.strftime("%Y-%m-%d"), 
    #             "title": title,
    #             "due_date": self.due_date}
    
    @staticmethod
    def customer_rentals_response(rental, video):
        return {"release_date": video.release_date.strftime("%Y-%m-%d"),
                "title": video.title,
                "due_date": rental.due_date.strftime("%a, %d %b %Y %X %z %Z")}

    # @staticmethod
    # def customer_with_due_date_response(rental, customer):
    #     return {"due_date": rental.due_date.strftime("%a, %d %b %Y %X %z %Z"),
    #             "name": customer.name,
    #             "phone": customer.phone,
    #             "postal_code": str(customer.postal_code)}
