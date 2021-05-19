from flask import Blueprint, request, jsonify
from werkzeug.wrappers import PlainRequest
from app import db
from flask.helpers import make_response
from models.customer import Customer
from models.video import Video
from datetime import date
import os
import requests

# set up blueprints
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
customer_bp = Blueprint("customers", __name__, url_prefix="/customers")