from flask import Blueprint, make_response, jsonify
from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

# -------------- CRUD for /customers ------------------------


@customers_bp("", methods=["GET"])
def get_all_customers():
    """
    Lists all existing customers and details about each customer.
    """
    customers = Customer.query.all()
    response = [customer.to_json() for customer in customers]
    return response


# -------------- CRUD for /videos ---------------------------
