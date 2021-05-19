from flask import Blueprint, request, make_response, jsonify
from app import db
from .models.video import Video
from .models.customer import Customer
from datetime import datetime

customer_bp = Blueprint("customer", __name__, url_prefix="/customer")
video_bp = Blueprint("video", __name__, url_prefix="/video")
