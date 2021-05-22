from flask import current_app
from sqlalchemy.sql.expression import true 
from app import db
from datetime import datetime 
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)  
    phone = db.Column(db.String, nullable=True) 
    # date/time when video was released 
    registered_at = db.Column(db.DateTime, \
        default=datetime.now(),
        nullable=False) 
    videos_checked_out_count = db.Column(db.Integer, default=0) 
    # Customer has many Rentals, and a Rental belongs to a customer 
    # this is the synthetic field - establishing where to look back to 
    # with backref
    rentals = db.relationship("Rental", backref="customer")

    def customer_to_json_response(self):
        '''
        Converts a Customer instance into JSON format
        Output: Returns a Python dictionary in the shape of JSON response 
        that the API returns in the route that is called (GET route).
        '''
        return  {"id": self.id,
                "name": self.name,
                "registered_at": self.registered_at.strftime("%a, %d %b \
                %Y %X %z"),
                "postal_code": str(self.postal_code),
                "phone": self.phone,
                "videos_checked_out_count": self.videos_checked_out_count
                } 
        
    @staticmethod
    def from_json_to_customer(request_body):
        '''
        Converts JSON request body into a new instance of Customer
        input: Takes in a dictionary in the shape of the JSON the API 
        receives. 
        '''
        new_customer = Customer(name=request_body["name"],
                                postal_code=request_body["postal_code"],
                                phone = request_body["phone"])
        return new_customer

