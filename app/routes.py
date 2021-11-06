import datetime
from typing import ChainMap
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")
customer_bp = Blueprint("customer_bp", __name__, url_prefix="/customers")
rental_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")


#Roslyn: Customer
@customer_bp.route("", methods=["GET", "POST"])
def handle_customers():
    customer_response = []
    if request.method == "GET":
        if request.args.get("sort") == "asc":
            customers = Customer.query.order_by(Customer.title.asc())
        elif request.args.get("sort") == "desc":
            customers = Customer.query.order_by(Customer.title.desc())
        else:
            customers = Customer.query.all()
        customer_response = [customer.to_dict() for customer in customers]
        return jsonify(customer_response), 200
    elif request.method == "POST":
        request_body = request.get_json()
        if "name" not in request_body or "phone" not in request_body or "postal_code" not in request_body:
            return make_response({"details": "Invalid data"}, 400) 
        new_customer = Customer(name=request_body["name"],
                        phone=request_body["phone"], 
                        postal_code=request_body["postal_code"],
                        register_at=datetime.utcnow())
        db.session.add(new_customer)
        db.session.commit()
        return make_response({"customer": new_customer.to_dict()}, 201)


#Areeba: Video 

# extra note