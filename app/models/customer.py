from flask import current_app
# from sqlalchemy.orm import relationship
from app import db


class Customer(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    # Needed to give this a default value of 0 so that it can be incrememted in the checkout endpoint:
    videos_checked_out_count = db.Column(db.Integer, default=0)

    # current_rentals = relationship('Video', secondary='rental')
    current_rentals = db.relationship('Video', secondary='rental')
                            

    def convert_to_json(self, rentals_list=None):

        response_body = {  
            "id": self.cust_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,  
            "videos_checked_out_count": self.videos_checked_out_count
        }

        if rentals_list != None:
            response_body["rentals"] = rentals_list

        return response_body