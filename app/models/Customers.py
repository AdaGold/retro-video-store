from flask import current_app
from app import db 


class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(64))
    customer_zip = db.Column(db.String(5))
    customer_phone = db.Column(db.String(14))
    register_at = db.Column(db.DateTime)
    #videos_checked_out = foreign keys of video objects in a list maybe? 


    def to_json(self):
        customer_dictionary = { "ID": self.customer_id, 
                                "Customer Name": self.customer_name, 
                                "Postal Code": self.customer_zip, 
                                "Phone Number": self.customer_phone, 
                                "Registered": self.register_at #this will need to be a function I think
                                }
        return customer_dictionary
