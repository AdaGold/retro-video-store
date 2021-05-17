from flask import current_app
from app import db 


class Customer(db.Model):
    __tablename__ = "customers"
    customer_id = db.Column(db.Interger, primary_key=True)
    customer_name = db.Column(db.String(64))
    customer_zip = db.Column(db.String(5))
    customer_phone = db.Column(db.String(14))
    register_at = db.Column(db.Datetime)
    #videos_checked_out = foreign keys of video objects in a list maybe? 

    
