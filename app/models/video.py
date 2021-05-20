from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
# from app.models.customer import Customer


Base = declarative_base()




class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    #do i need the db?
    customers = db.relationship("Rental", back_populates="renters")
#OR
    # customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    # customer = db.relationship("Rental", backref=db.backref("renters"))
    __tablename__ = "Video"

    # def calc_available_inventory():
    #     pass

    def api_response(self): 
        response_body = {
                        "id": self.id,
                        "title": self.title,
                        "release_date": self.release_date,
                        "total_inventory": self.total_inventory,
                        #below needs to be changed
                        "available_inventory": 0
                        # "available_inventory": calc_available_inventory()
                        }

        return response_body

