from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
# from sqlalchemy import desc, asc 
from datetime import datetime
import requests
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = [customer.to_dict() for customer in customers]
    return jsonify(customers_response)

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return customer.to_dict()
    return (f"No customer with ID #{customer_id} found", 404)

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    if check_for_valid_input(request_body):
        new_customer = Customer(name = request_body["name"],
                        postal_code = request_body["postal_code"],
                        phone = request_body["phone"])
        new_customer.registered_at = datetime.utcnow()
        db.session.add(new_customer)
        db.session.commit()
        return ({"id": new_customer.customer_id}, 201) 
    return ({"details": "Invalid data"}, 400)

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    # need to include a way to return 400 error if 
    # any of the request body fields are missing or invalid
    # (or example if the videos_checked_out_count is not a number)
    customer = Customer.query.get(customer_id)
    if customer:
        form_data = request.get_json()
        if check_for_valid_input(form_data):
            customer.name = form_data["name"]
            customer.postal_code = form_data["postal_code"]
            customer.phone = form_data["phone"]
            db.session.commit()
            return customer.to_dict()
            # return make_response((customer.to_dict()), 200)
        #probably need to get more specific with the 400 message
        return ({"details": "Invalid data"}, 400)
        # return ("Invalid input", 400)
    # return ("", 404)
    return make_response(f"No customer with ID #{customer_id} found", 404)
    

# this function probably needs to be more detailed and
# might need to include check_out info, etc
# this function could be built out so it does...
# if not "name" in form_data
#   return ("specific details of error")
def check_for_valid_input(form_data):
    if "name" in form_data and "postal_code" in form_data and "phone" in form_data:
        return True 
    return False

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return make_response({"id": customer.customer_id}, 200)
    return make_response(f"No customer with ID #{customer_id} found", 404)