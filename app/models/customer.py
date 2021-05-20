from flask import current_app
from sqlalchemy.orm import relationship
from app import db


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    registered_at = db.Column(db.DateTime)
    # ideally this would be a list of video ids:
    videos_of_customer = db.relationship('Video', 
                            secondary='link' 
                            )

    def convert_to_json(self):

        response_body = {  
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            # the following will be the # of ids in videos_of_customer:  
            # "videos_checked_out_count":  
        }


        return response_body