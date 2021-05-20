from flask import current_app
from app import db
from app.models.customer import Customer
from app.models.video import Video


# class Video(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
#     title = db.Column(db.String)
#     release_date = db.Column(db.DateTime)
#     total_inventory = db.Column(db.Integer)