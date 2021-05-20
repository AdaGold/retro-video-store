from app import db
import datetime
from flask import current_app
from sqlalchemy import Table, Column, Integer, ForeignKey


# this is telling flask about my database task table

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime(), nullable=True)
    total_inventory = db.Column(db.Integer)
    