from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.video import Video
import os
import requests

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

