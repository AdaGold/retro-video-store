from flask import current_app
from app import db
from flask import request, Blueprint, make_response, jsonify

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    release_date = db.Column(db.DateTime, nullable = True)
    total_inventory = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)