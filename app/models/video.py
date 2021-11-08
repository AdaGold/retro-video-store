# from flask import current_app
from app import db
from sqlalchemy.schema import FetchedValue

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer", secondary="videos_customers", backref="videos")
    inventory_checked_out = db.Column(db.Integer) 

    def to_dict(self):
        return {
                "title": self.title,
                "id": self.id,
                "release_date": self.release_date,
                "total_inventory": self.total_inventory
                }