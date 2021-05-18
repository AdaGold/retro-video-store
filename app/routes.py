from app import db
from app.models.customer import Customer
from datetime import datetime
from flask import request, Blueprint, make_response, jsonify
import requests
import os
from app.models.video import Video

videos_bp = Blueprint(
    "videos", __name__, url_prefix="/videos")
customers_bp = Blueprint(
    "customers", __name__, url_prefix="/customers")

# ---------------------------
# WAVE 1 - CUSTOMER ENDPOINTS
# ---------------------------


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customer_index():
    customers = Customer.query.all()
    customers_response = [(customer.to_json()) for customer in customers]
    return make_response(jsonify(customers_response), 200)


@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_body = request.get_json()
    if "name" in request_body and "postal_code" in request_body and "phone" in request_body:
        new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"]
        )
        customer.registered_at = datetime.now()
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({new_customer.to_json()}), 201
    else:
        return make_response({"details": "Invalid data: you must include a name, postal code, and phone number"}, 400)


@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("Customer does not exist", 404)
    return jsonify({customer.to_json()}), 200


@customer_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    form_data = request.get_json()
    if customer is None:
        return make_response("Customer does not exist", 404)
    elif "name" in form_data and "postal_code" in form_data and "phone" in form_data:
        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]
        db.session.commit()
        return jsonify({"customer": customer.to_json()}), 200
    return make_response("Bad Request", 400)


@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("Customer does not exist", 404)
    else:
        db.session.delete(customer)
        db.session.commit()
        customer_response = {
            "details": f'Task {task.task_id} "{task.title}" successfully deleted'}
    return make_response(customer_response), 200


# --------------------------
# WAVE 1 - VIDEO ENDPOINTS
# --------------------------
