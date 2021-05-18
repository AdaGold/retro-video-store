from flask import current_app
from app import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True)
    total_inventory = db.Column(db.Integer)

    def build_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "release_date" : self.release_date,
            "total_inventory" : self.total_inventory
        }
