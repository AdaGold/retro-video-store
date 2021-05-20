from flask import current_app
from sqlalchemy.sql.expression import true 
from app import db
from datetime import datetime #added -  I need it for register_at
# from sqlalchemy.orm import relationship # when should this be used?


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.Integer, nullable=False) # can be null? 
    phone = db.Column(db.String, nullable=True) # DOUBLE CHECK
    # date/time when video was released - now?
    registered_at = db.Column(db.DateTime, \
        default=datetime.now(),
        nullable=False) 
    videos_checked_out_count = db.Column(db.Integer, default=0) 
    # rentals = Customer has many Rentals, and a Rental belongs to a customer
    # this is the fake field     # Establishing relationship 
    rentals = db.relationship("Rental", backref="customer")

    # what is the difference btw the lines below and line 13?
    # register_at = db.Column(db.DateTime, server_default=db.func.current_timestamp()) 

    def customer_to_json_response(self):
        '''
        Converts a Customer instance into JSON format
        Output: Returns a Python dictionary in the shape of JSON response 
        that the API returns in the route that is called (GET route).
        '''
        return  {"id": self.id,
                "name": self.name,
                "registered_at": self.registered_at.strftime("%a, %d %b %Y %X %z"),
                "postal_code": str(self.postal_code),
                "phone": self.phone,
                "videos_checked_out_count": self.videos_checked_out_count
                } # Whyyyyyyy did I have to change it to INT?????
                
    @staticmethod
    def from_json_to_customer(request_body):
        '''
        Converts JSON request body into a new instance of Customer
        input: Takes in a dictionary in the shape of the JSON the API 
        receives. 
        '''
        # could add an if to check that the request body is good -
        # then create customer
    
        new_customer = Customer(name=request_body["name"],
                postal_code=request_body["postal_code"],
                phone = request_body["phone"])

        return new_customer
    
    # def register_customer(self):   
    #     '''
    #     Updates the attribute registered_at of the instance of a customer
    #     to the current date/time in the .strftime format 
    #     "Wed, 16 Apr 2014 21:40:20 -0700".
    #     '''
    #     register_time = (datetime.now()).strftime("%a, %d %b %Y %X %z")  
    #     self.registered_at = register_time 
        # need to call on a post method when registering a new 
        # new customer


    # def goal_to_json_response(self):
    #     '''
    #     Converts a Goal's instance into JSON response
    #     Output: Returns a Python dictionary in the shape JSON response
    #     for only one goal.
    #     '''
    #     return {"goal": 
    #                     {"id": self.goal_id,
    #                     "title": self.title}}

    # def simple_response(self):
    #     '''
    #     Converts a Goals's instance columns (atributes) into JSON response
    #     including the foreign key goal id.
    #     Output: Returns a Python dictionary in the shape JSON response 
    #     for a goal.
    #     '''
    #     return {"id": self.goal_id,
    #             "title": self.title}

#     def customer_to_json_response(self):
#         return 
#         '''
#         Converts a Task's instance into JSON response
#         Output: Returns a Python dictionary in the shape JSON response
#         for only one task.
#         '''
#         return {"id": self.id,
#                 "title": self.title,
#                 "description": self.description,
#                 "is_complete": bool(self.completed_at)}

#     # for registered at: the format should be
#     #  "Wed, 29 Apr 2015 07:54:14 -0700"
#     [{
#     "id": self.id,
#     "name": self.name,
#     "registered_at": self.datetime_added,
#     "postal_code": self.zip_code,
#     "phone": self.phone_number,
#     "videos_checked_out_count": 0
#   },
#   {
#     "id": 2,
#     "name": "Curran Stout",
#     "registered_at": "Wed, 16 Apr 2014 21:40:20 -0700",
#     "postal_code": "94267",
#     "phone": "(908) 949-6758",
#     "videos_checked_out_count": 0
#   }
# ]


