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
        is_complete = check_customer_post(request_body)
        if is_complete:
            return is_complete
        new_customer = Customer(name=request_body["name"],
                            phone=request_body["phone"], 
                            postal_code=request_body["postal_code"],
                            register_at=datetime.utcnow())
        db.session.add(new_customer)
        db.session.commit()
        return make_response(new_customer.to_dict(), 201)

@customer_bp.route("/<customer_id>", methods=["GET", "DELETE", "PUT"])
def handle_customer(customer_id):
    if not customer_id.isnumeric():
        return make_response({"message" : "Please enter a valid customer id"}, 400)
    customer = Customer.query.get(customer_id)
    if request.method == "GET":
        if not customer:
            return make_response({"message" : f"Customer {customer_id} was not found"}, 404)
        return make_response(customer.to_dict(),200)
    elif request.method == "DELETE":
        if not customer:
            return make_response({"message" : f"Customer {customer_id} was not found"}, 404)
        db.session.delete(customer)
        db.session.commit()
        return make_response({"id": int(customer_id)}, 200)
    elif request.method == "PUT":
        if not customer:
            return make_response({"message" : f"Customer {customer_id} was not found"}, 404)
        request_body = request.get_json()
        customer.name = request_body["name"] if "name" in request_body else customer.name
        customer.phone = request_body["phone"] if "phone" in request_body else customer.phone
        customer.postal_code = request_body["postal_code"] if "postal_code" in request_body else customer.postal_code
        db.session.commit()
        return make_response({"customer": customer.to_dict()}, 200)


def check_customer_post(request_body):
    if "name" not in request_body:
        return make_response({"details": "Request body must include name."}, 400)
    elif "phone" not in request_body:
        return make_response({"details": "Request body must include phone."}, 400)
    elif "postal_code" not in request_body:
            return make_response({"details": "Request body must include postal_code."}, 400)
    else:
        return False


#Areeba: Video 

# extra note