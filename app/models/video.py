from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship, back_populate
# from app.models.customer import Customer
# from app.models.rental import Rental

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    customers = db.relationship("Rental", back_populates="video")


#all other options i saw???
    # # customer = db.relationship("Customer", secondary="orders")
    # rentals = db.relationship('Rental', backref='videos', lazy=True)


    # rentals = db.relationship('Customer', secondary="rentals", lazy='subquery',backref=db.backref('rentals', lazy=True))

    # renters = relationship("Rental", back_populates="video", lazy = True)
    # customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))


    def api_response(self): 
        response_body = {
                        "id": self.id,
                        "title": self.title,
                        "release_date": self.release_date,
                        "total_inventory": self.total_inventory,
                        "available_inventory": self.total_inventory
                        }

        return response_body

