from flask import Blueprint, request, jsonify
from app import db
from .models.customer import Customer
from .models.video import Video
from datetime import datetime
import requests
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

def customer_not_found(func):
    def inner(customer_id):
        if Customer.query.get(customer_id) is None:
            return jsonify(None), 404
        return func(customer_id)
    #renames the function for each wrapped endpoint to avoid endpoint conflict
    inner.__name__ = func.__name__
    return inner

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers_index():
    customers = Customer.query.all()
    customers_response = [customer.to_json() for customer in customers]
    return jsonify(customers_response), 200

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
@customer_not_found
def single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    return jsonify(customer.to_json()), 200

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_body = request.get_json()
    new_customer = Customer(name = request_body["name"],
                    postal_code = request_body["postal_code"],
                    phone = request_body["phone"],
                    registered_at = request_body["registered_at"],
                    videos_out_count = request_body["videos_out_count"])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(new_customer.to_json()), 201