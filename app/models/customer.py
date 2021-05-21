from flask import current_app
from app import db
from datetime import datetime

# # association table for many to many relationship between customer and video
# association_table = db.Table('customer_videos',
#     db.Column('customer_id', db.Integer, db.ForeignKey('customer.customer_id')),
#     db.Column('video_id', db.Integer, db.ForeignKey('video.video_id'))
# )


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    postal_code = db.Column(db.Integer)
    phone = db.Column(db.String) 
    register_at = db.Column(db.DateTime, nullable=True)
    videos_checked_out_count = db.Column(db.Integer, server_default=db.text("0"))
    
    #establish relationship
    rentals = db.relationship('Rental', backref='customer', lazy = True)

    def details_of_customer_response(self):
        return {
                "id": self.customer_id,
                "name": self.name,
                "registered_at": self.register_at,
                "postal_code": self.postal_code,
                "phone": self.phone,
                "videos_checked_out_count": len(self.rentals)
                }

    def add_new_customer(self):
        return{
            
            "name": self.name,
            "postal_code": self.postal_code,
            "phone": self.phone_number
        }
