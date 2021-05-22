from flask import current_app
from app.models.customer import Customer
from app import db


class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    current_renters = db.relationship('Customer', secondary='rental')                        

    def convert_to_json(self):

        response_body = {  
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }

        return response_body


# ❗️ Is it okay that I put this join table in this file?
class Rental(db.Model): 
    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_video_id = db.Column(db.Integer, db.ForeignKey('video.video_id'))
    fk_customer_id = db.Column(db.Integer, db.ForeignKey('customer.cust_id'))
    due_date = db.Column(db.DateTime)

    # ❗️ backref here is declaring a 'rental' property for both the Customer and Video classes, but I'm not sure when or if that's being used
    customer = db.relationship('Customer', backref='rental') 
    video = db.relationship('Video', backref='rental')

    # ❗️ pointless - lol I think I use this once
    def convert_to_json(self):

        response_body = {  
            "rental_id": self.rental_id
        }

        return response_body

