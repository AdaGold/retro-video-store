from flask import current_app
from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .customer import Customer

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True, default=None)
    total_inventory = db.Column(db.Integer)

    def get_response(self):
        return {
            "id":self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": int(self.total_inventory)}
            # "available_inventory":0 