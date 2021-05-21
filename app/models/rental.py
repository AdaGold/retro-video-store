from flask import current_app
from app import db
from datetime import datetime 

class Rental():
    rental_id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime, nullable=False)

def checkout_video(self):
        return {
                "due_date": self.due_date
            }