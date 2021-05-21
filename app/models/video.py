
from flask import Flask, current_app
from app import db
from flask_sqlalchemy import SQLAlchemy


class Video(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    title = db.Column(db.String)
    release_date = db.Column(db.Datetime)
    total_inventory = db.Column(db.Interger)
# - title of the video
# - release date datetime of when the video was release_date
# - total inventory of how many copies are owned by the video store
