# from flask import current_app
from app import db
from app.models.rental import Rental


def set_to_total_inventory(context):
    return context.get_current_parameters()["total_inventory"]

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer, default=0)
    available_inventory = db.Column(db.Integer, default=set_to_total_inventory) 
    rentals_out = db.relationship("Rental", backref="video") #is lazy=True needed?


    def return_data(self):
        return_info = {
                "id": self.id,
                "title": self.title,
                "release_date": self.release_date,
                "total_inventory": self.total_inventory,
                "available_inventory": self.available_inventory
            }
        return return_info