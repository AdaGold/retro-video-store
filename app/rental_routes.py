from app import db
from flask import Blueprint, request, jsonify
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video


rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# @rentals_bp.route("/check-out",methods=["POST"], strict_slashes=False)
# def check_out_rental():