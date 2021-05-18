from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from datetime import datetime
import os 
from dotenv import load_dotenv

load_dotenv()

# ===== Customers ===================================================
customers_bp = Blueprint("customer", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])

@customers_bp.route("", methods=["POST"])
def post_customers():
    pass

@customers_bp.route("/<id>", methods=["GET"])
def get_customer(active_id):
    pass

@customers_bp.route("/<id>", methods=["PUT"])
def put_customer(active_id):
    pass

@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(active_id):
    pass

# ===== Videos ======================================================
videos_bp = Blueprint("video", __name__, url_prefix="/videos")

# ===== Rentals =====================================================