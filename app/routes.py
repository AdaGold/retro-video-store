from flask import Blueprint, request, jsonify
from werkzeug.wrappers import PlainRequest
from app import db
from flask.helpers import make_response
from models.customer import Customer
from models.video import Video
from datetime import date
import os
import requests

# set up blueprints
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
customer_bp = Blueprint("customers", __name__, url_prefix="/customers")

# helper function to check that customer/video ids are integers
def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

# Wave 1: CRUD (Create, Read, Update & Delete) for customer
@customer_bp.route("", methods=["GET"], strict_slashes=False)
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

@customer_bp.route("/<id>", methods=["GET"], strict_slashes=False)
def get_one_customer(id):
    if not is_int(id):
        return {
            "message": f"ID {id} must be an integer",
            "success": False
        }, 400
    
    customer = Customer.query.get(id)

    if customer is None:
        return make_response("", 404)
    else:
        return {
            "customer": customer.to_json()
        }, 200

@customer_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    try:
        request_body = request.get_json()

        new_customer = Customer(id=request_body["id"],
                                name=request_body["name"],
                                postal_code=request_body["postal_code"],
                                phone=request_body["phone"])
        db.sesssion.add(new_customer)
        db.session.commit()

        return new_customer.to_json(), 200
    
    except KeyError:
        return{"details": "Invalid data"}, 400

@customer_bp.route("/<id>", methods=["PUT"], strict_slashes=False)
def update_customer(id):

    customer = Customer.query.get(id)

    if customer:
        customer_data = request.get_json()

        customer.name = customer_data["name"]

        db.session.commit()

        return {
            "customer": customer.to_json()
        }, 200
    else:
        return make_response("", 404)

@customer_bp.route("/<id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(id):

    customer = Customer.query.get(id)

    if customer is None:
        return make_response("", 404)
    else:
        db.session.delete(customer)
        db.session.commit()

        return {
            "details": f'Customer {customer.id} successfully deleted'
        }