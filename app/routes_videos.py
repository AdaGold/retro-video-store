from flask import Blueprint, request, jsonify, make_response
from app import db 

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")