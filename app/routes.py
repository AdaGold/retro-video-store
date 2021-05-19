from flask import request, Blueprint
from app import db
from flask import jsonify
from .models.customer import Customer
import requests
import os

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customer_bp.route("", methods=["POST"], strict_slashes=False)
def add_task():
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return jsonify({
        "details": "Invalid data"
        }), 400
    new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"])
    
    db.session.add(new_customer)
    db.session.commit()
    return new_customer.to_json(), 201

@customer_bp.route("", methods=["GET"], strict_slashes=False)
def customer_index():
    customers = Customer.query.all()
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_json())

    return jsonify(customer_response), 200


