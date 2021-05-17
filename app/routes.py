from flask import Blueprint, request, make_response
from .models.customer import Customer
from .models.video import Video
from flask import jsonify
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


@customers_bp.route("", methods=["GET"])
def get_customer():
    customers = Customer.query.all()

