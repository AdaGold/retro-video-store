from app import db
from flask import Blueprint, request, jsonify
from app.models.rental import Rental
# from datetime import datetime

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")