from flask import request, Blueprint, make_response, jsonify
from app import db
from dotenv import load_dotenv
from app.models.customer import Customer

load_dotenv()

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

