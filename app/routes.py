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
    request_body = request.get_json()
    try:
        new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
            register_at=datetime.now()
        )
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.to_dict(), 201)

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