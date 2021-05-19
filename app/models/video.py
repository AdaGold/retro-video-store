# from flask import current_app
from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer, nullable = True)
    available_inventory = db.Column(db.Integer, nullable = True)


    def return_data(self):
        return_info = {
                "id": self.id,
                "title": self.title,
                "release_date": self.release_date,
                "total_inventory": self.total_inventory,
                "available_inventory": self.available_inventory
            }
        return return_info