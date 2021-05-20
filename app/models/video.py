from flask import current_app
from app import db
# from app.models.goal import Goal

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer)

    def calc_available_inventory():
        pass

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

