from flask import current_app
from app import db
from flask import request, Blueprint, make_response, jsonify

def my_default(context):
    return context.get_current_parameters()['total_inventory']

class Video(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    release_date = db.Column(db.DateTime, nullable = True)
    total_inventory = db.Column(db.Integer, default = 0, nullable = False)
    available_inventory = db.Column(db.Integer, default = my_default)

