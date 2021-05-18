# Videos are entities that describe a video at the video store. They contain:

# title of the video
# release date datetime of when the video was release_date
# total inventory of how many copies are owned by the video store

from flask import current_app
from app import db

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title_of_video = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    total_inventory = db.Column(db.Integer)

# class FooBarJoin(db.Model):
#     foo_id = db.Column(db.Integer, db.ForeignKey('foo.id'), primary_key=True)
#     bar_id = db.Column(db.Integer, db.ForeignKey('bar.id'), primary_key=True)