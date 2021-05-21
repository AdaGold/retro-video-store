
from operator import countOf
from flask import current_app
from app import db
from .customer import Customer



class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    customers_rented_to = db.Column(db.Integer, db.ForeignKey('customer.id'),nullable=True)

    def calculate_inventory(self):
        if self.customers_rented_to:
            self.available_inventory =  self.total_inventory - len([customer.id for customer in self.customers_rented_to])
        else:
            self.available_inventory = self.total_inventory
        return self.available_inventory


    def build_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "release_date" : self.release_date,
            "total_inventory" : self.total_inventory, 
            "available_inventory" : self.calculate_inventory()
        }
