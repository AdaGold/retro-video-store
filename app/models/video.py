
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
        print(self.customers_rented_to)
        if self.customers_rented_to:
            return self.total_inventory - len([i for i in self.customers_rented_to])
        else:
            return self.total_inventory

    def build_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "release_date" : self.release_date,
            "total_inventory" : self.total_inventory, 
            "available_inventory" : self.available_inventory
        }
