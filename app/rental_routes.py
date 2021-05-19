from app import db, helper
#from .models.customer import Customer
from .models.video import Video
from flask import request, Blueprint, make_response, jsonify, Response
from sqlalchemy import desc, asc
from datetime import date
import os
import requests
import json

rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


