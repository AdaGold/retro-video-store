from flask import current_app
from app import db

# def default_available_inventory(context):
#     return context.get_current_parameters()['total_inventory']

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime, nullable=True, default=None)
    total_inventory = db.Column(db.Integer)
    # available_inventory = db.Column(db.Integer, default=default_available_inventory)

    active_rentals = db.relationship('Rental', backref='videos', lazy=True)



    def get_response(self):
        return {
            "id":self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": int(self.total_inventory),
            "available_inventory": self.total_inventory - len(self.active_rentals)}