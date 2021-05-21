from flask import current_app
from app import db
from flask_sqlalchemy import SQLAlchemy

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)
    #set available_inventory = self.total_inventory - len(self.customers)??
    available_inventory = db.Column(db.Integer)
    customers = db.relationship("Rental", back_populates="video")
    __tablename__ = "videos"

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory,
            "available_inventory": self.available_inventory
        }