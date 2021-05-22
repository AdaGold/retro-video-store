from datetime import datetime
from flask import Blueprint, make_response, request, jsonify
from app import db
from app.models.customer import Customer
from app.models.video import Video
import os
import requests

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

                                       ### Crud Customers ###
@customers_bp.route("", methods=["GET"])
def list_all_customers():
    customers = Customer.query.all()
    
    return jsonify([customer.get_customer_info for customer in customers]) 


@customers_bp.route("", methods=["POST"])
def add_new_customer():
    request_body = request.get_json()

    if invalid_data(request_body):
        return make_response({"details": "invalid data"}, 400)

    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"]
        )
    db.session.add(new_customer)
    db.session.commit()

    return make_response({"id": new_customer.customer_id}, 201)

def invalid_data(request_body):
    if ("name" not in request_body or "postal_code" not in request_body or "phone" not in request_body):
        return True
    return False


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer_id(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response({"details": ("Customer not in the system... Want to become a member?")}, 404)

    return jsonify(customer.resp_json())

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
   
    if customer is None:
        return make_response({"details":("Customer not a member")}, 404)
        
    request_body = request.get_json()
    
    try: 
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
    except KeyError:
        return make_response({"details":("invalid data")}, 400)
    db.session.commit()

    return make_response(customer.resp_json(), 200)

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response({"details":("Customer not in the system")}, 404)
    
    db.session.delete(customer)
    db.session.commit()

    return {
        "id": f"Customer {customer.customer_id} has been erased from the universe!"
    }, 200


                                              ### Crud Customers ###

@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    return jsonify([video.get_video_info() for video in videos])

@videos_bp.route("", methods=["POST"])
def post_new_video():
    request_body = request.get_json()

    if invalid_data(request_body):
        return make_response({"details": "invalid data"}, 400)

    video = Video(
        title= request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"]
        )
    db.session.add(video)
    db.session.commit()

    return make_response({"id": video.video_id}, 201)

@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    pass