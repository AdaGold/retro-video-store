from flask import request, Blueprint
from app import db
from flask import jsonify
from .models.customer import Customer
from .models.video import Video
import requests
import os

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")


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

@customer_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        found_customer = customer.to_json()
        return jsonify(found_customer), 200
    return "", 404

@customer_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        request_body = request.get_json()
        if "name" in request_body and "postal_code" in request_body and "phone" in request_body:
            customer.name = request_body["name"]
            customer.postal_code = request_body["postal_code"]
            customer.phone = request_body["phone"]
            db.session.commit()
            updated_customer = customer.to_json()
            return jsonify(updated_customer), 200
        return jsonify({
        "details": "Invalid data"
        }), 400
    return "", 404
  
@customer_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({
        "id": customer.customer_id
        }), 200
    return "", 404

