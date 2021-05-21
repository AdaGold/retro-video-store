from flask import Blueprint
from flask.signals import request_finished
from app import db
from flask import request, make_response, jsonify
from datetime import datetime
from app.models.customer import Customer
from app.models.video import Video
import os
import requests

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# Wave 1 Customer routers
# Lists all existing customers and details about each customer. No arguments
@customer_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        # building a list of jsons by calling to_json on each task
        customers_response.append(customer.to_json())

    return jsonify(customers_response)


# Gives back details about specific customer with required argument "id"
@customer_bp.route("/<customer_id>", methods=["GET"])
def get_specific_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("", 404)
    else:
        return make_response(customer.to_json(), 200)


# Creates a new video with the params "name", "postal_code", "phone"
@customer_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    required_properties = ["name", "postal_code", "phone"]
    for prop in required_properties:
        if prop not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        
    new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone_number=request_body["phone"])

    db.session.add(new_customer)
    db.session.commit() 
    
    # returning single customer created by calling to_json on new customer
    return make_response({"id": new_customer.customer_id}, 201)


# Updates and returns details about specific customer with params "name", "postal_code", and "phone"
@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    customer_data = request.get_json()

    if customer is None:
        return make_response("", 404)

    if ("name" or "postal_code" or "phone") not in customer_data:
        return make_response({"details": "Invalid data"}, 400) 
    else:
        customer.name=customer_data["name"]
        customer.postal_code=customer_data["postal_code"]
        customer.phone_number=customer_data["phone"]
        
        db.session.commit()
        return make_response(customer.to_json(), 200)


@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("", 404)
    else:
        db.session.delete(customer)
        db.session.commit()
        
        return make_response({"id": customer.customer_id}, 200)


# Wave 1 Video routes
@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        # building a list of jsons by calling to_json on each task
        videos_response.append(video.to_json())

    return jsonify(videos_response)


@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    required_properties = ["title", "release_date", "total_inventory"]
    for prop in required_properties:
        if prop not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        
    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit() 
    
    # returning single task created by calling to_json on new task
    return make_response({"id": new_video.video_id}, 201)


@video_bp.route("/<video_id>", methods=["GET"])
def get_videos(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response("", 404)
    else:
        return make_response(video.to_json())


@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response("", 404)
    elif request.method == "PUT":
        video_data = request.get_json()
        video.title = video_data["title"]
        video.release_date = video_data["release_date"]
        video.total_inventory = video_data["total_inventory"]
        
        db.session.commit()
        return make_response(video.to_json(), 200)
        

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    
    if video is None:
        return make_response("", 404)
    else:
        db.session.delete(video)
        db.session.commit()
        
        return make_response({"id": video.video_id}, 200)


# Wave 2 Rental routes