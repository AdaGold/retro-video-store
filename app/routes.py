from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
# from sqlalchemy import desc, asc 
from datetime import datetime
import requests
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET"])
def get_customers():
    pass 