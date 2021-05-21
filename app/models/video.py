from flask import current_app
# ❗️ wondering if I can get rid of this import and use db.relationship
from sqlalchemy.orm import backref, relationship
from app.models.customer import Customer
from app import db


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    current_renters = relationship('Customer', secondary='rental')                        

    def convert_to_json(self):
        # available_inventory = (self.total_inventory) - (# of renters)
        # available_inventory = self.total_inventory 

        response_body = {  
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
            # "available_inventory": available_inventory
        }

        return response_body


# ❗️ Is it okay that I put this join table in this file?
class Rental(db.Model): 
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # ❗️ I'm not sure that the primary_key=True parameter is necessary here, or what it's doing
    fk_video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'), primary_key=True)
    fk_customer_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'), primary_key=True)

    # backref here is declaring a 'rental' property for both the Customer and Video classes
    customer = relationship(Customer, backref=backref('rental')) 
    video = relationship(Video, backref=backref('rental'))
