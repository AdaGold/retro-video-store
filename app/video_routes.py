from app import db
from flask import Blueprint, request, jsonify
from app.models.video import Video

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")