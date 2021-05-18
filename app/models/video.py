from flask import current_app
from app import db
from datetime import datetime
# from .rentals import Rentals


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    inventory_total = db.Column(db.Integer)
    # rented_to = db.relationship('Customer', 
    #     secondary=Rentals, 
    #     back_populates='checked_out')

    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "release_date" : self.release_date,
            "inventory_total" : self.inventory_total,
            "available_inventory" : self.inventory_total
        }