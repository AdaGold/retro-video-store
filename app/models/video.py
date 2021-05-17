# Videos are entities that describe a video at the video store. They contain:

# title of the video
# release date datetime of when the video was release_date
# total inventory of how many copies are owned by the video store

from flask import current_app
from app import db

class Video(db.Model):
    title = db.Column(db.String, primary_key=True)
    completed_at = db.Column(db.DateTime, nullable = True)
    total_inventory = db.Column(db.Integer)
