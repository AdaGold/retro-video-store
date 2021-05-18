from flask import current_app 
from app import db
from datetime import datetime #added -  I need it for register_at
# from sqlalchemy.orm import relationship # when should this be used?


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    postal_code = db.Column(db.String, nullable=False) # can phone be null? 
    phone = db.Column(db.String, nullable=True) # DOUBLE CHECK
    register_at = db.Column(db.DateTime, default=datetime.utcnow(),  
        nullable=False) # check if utcnow() is the right format
    
    # what is the difference btw line 10 and 13?
    # register_at = db.Column(db.DateTime, server_default=db.func.current_timestamp()) # database more efficient?
    # register_at = db.Column(db.DateTime, default=datetime.now().strftime("%c"))  
    # has to look like this "Wed, 16 Apr 2014 21:40:20 -0700"

    # Establishing many-to-many relationship 
    # or is it  relationship("Video", secondary= ...) - call CHO
    videos = db.relationship("Video", secondary="rental", lazy=True) # how abbout lazy=true?

    # Establishing one-to-many relationships to Task Model
    # tasks = db.relationship('Task', backref="goal", lazy=True) # ask about backref

    
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


