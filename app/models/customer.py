from flask import current_app
from app import db

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    # ❗️ Check in Postman the date time is a string in the response body
    registered_at = db.Column(db.DateTime)
    # videos_checked_out_count = 

    def convert_to_json(self, cust_list=None):

        response_body = {  
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone,
            # "videos_checked_out_count": ? 
        }

        # if cust_list != None:
        #     response_body["customer"] = cust_list

        return response_body