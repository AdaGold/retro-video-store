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