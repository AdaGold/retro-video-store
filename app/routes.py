from flask import Blueprint, request, jsonify
from werkzeug.wrappers import PlainRequest
from app import db
from flask.helpers import make_response
from models.customer import Customer
from models.video import Video
from datetime import datetime
import os
import requests

# set up blueprints
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

# helper function to check that customer/video ids are integers
def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

# Wave 1: CRUD (Create, Read, Update & Delete) for customer
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customer():
    customer_name_from_url = request.args.get("name")
    # get customer by name
    if customer_name_from_url:
        customers = Customer.query.filter.by(name=customer_name_from_url)
    # get all customers
    else:
        customers = Customer.query.all()
    
    customers_response = []

    for customer in customers:
        customers_response.append(customer.to_json())
    
    return jsonify(customers_response), 200

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_one_customer(customer_id):
    if not is_int(customer_id):
        return {
            "message": f"ID {customer_id} must be an integer",
            "success": False
        }, 400
    
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("Customer does not exist", 404)
    else:
        return {
            "customer": customer.to_json()
        }, 200

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    try:
        request_body = request.get_json()

        new_customer = Customer(name=request_body["name"],
                                postal_code=request_body["postal_code"],
                                phone=request_body["phone"],
                                registered_at=datetime.now())
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({
            "id": new_customer.customer_id
        }), 201
    
    except KeyError:
        return make_response({"details": "Invalid data - please include a name, postal code and phone number"}, 400)

@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer:
        customer_data = request.get_json()

        customer.name = customer_data["name"]
        customer.postal_code = customer_data["postal_code"]
        customer.phone = customer_data["phone"]
        
        db.session.commit()

        return jsonify(customer.to_json()), 200
    else:
        return make_response({"error": "Bad Request"}, 400)

@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("Customer does not exist", 404)
    else:
        db.session.delete(customer)
        db.session.commit()

        return jsonify({
            "id": customer.customer_id
        }), 200

# # Wave 1: CRUD (Create, Read, Update & Delete) for video
# @video_bp.route("/<id>", methods=["GET"], strict_slashes=False)
# def