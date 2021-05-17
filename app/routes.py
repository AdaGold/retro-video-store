from flask import Blueprint
from app.models.Videos import Video 
from app.models.Customers import Customer
from flask import Blueprint, make_response, jsonify, request
from app import db 
from datetime import datetime
import requests 
import os 

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

def return_404():
    return make_response("Whatever you are looking for, we didn't find it.", 404)

def update_customer_from_json(body):
    pass


@customer_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_json())
    
    return jsonify(customer_response), 200

@customer_bp.route("/<customer_id>", methods=["GET"])
def get_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return return_404()
    else:
        return make_response(customer.to_json(), 200)

@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return return_404()
    else:
        request_body = request.get_json()
        try:
            customer.customer_name = request_body["name"]
            customer.customer_zip = request_body["postal_code"]
            customer.customer_phone = request_body["phone"]
        
        except KeyError:
            return make_response({"That didn't work.": "Invalid data or format."}, 400)
        
        db.session.commit()

        return make_response(customer.to_json(), 201)




@customer_bp.route("", methods=["POST"])
def post_new_customer():
    request_body = request.get_json()
    try:
        new_customer = Customer(customer_name=request_body["name"], customer_zip=request_body["postal_code"], customer_phone=request_body["phone"], register_at=datetime.now())
    except KeyError:
        return make_response({"That didn't work.": "Invalid data or format."}, 400)
    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.to_json(), 201)