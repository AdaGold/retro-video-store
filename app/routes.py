from flask import Blueprint, request, jsonify
from app import db
from .models.customer import Customer
from .models.video import Video
from datetime import datetime
import requests
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

def customer_not_found(func):
    def inner(customer_id):
        if Customer.query.get(customer_id) is None:
            return jsonify({"details": "Customer not found"}), 404
        return func(customer_id)
    inner.__name__ = func.__name__
    return inner

def video_not_found(func):
    def inner(video_id):
        if Video.query.get(video_id) is None:
            return jsonify({"details": "Video not found"}), 404
        return func(video_id)
    #renames the function for each wrapped endpoint to avoid endpoint conflict
    inner.__name__ = func.__name__
    return inner

#---------------------# CUSTOMER ENDPOINTS #---------------------#

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers_index():
    customers = Customer.query.all()
    customers_response = [customer.to_json() for customer in customers]
    return jsonify(customers_response), 200

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
@customer_not_found
def single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    return jsonify(customer.to_json()), 200

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return jsonify({"details": "Invalid Data"}), 400
    new_customer = Customer(name = request_body["name"],
                    postal_code = str(request_body["postal_code"]),
                    phone = str(request_body["phone"]),
                    registered_at = datetime.now(),
                    #modify this line or Customers model to actually work (but in theory a new customer added should have a video_out_count of 0)
                    videos_checked_out_count = 0)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(new_customer.to_json()), 201

@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
@customer_not_found
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    response_body = request.get_json()
    if "name" not in response_body or "postal_code" not in response_body or "phone" not in response_body:
            return jsonify({"details": "Invalid Data"}), 400
    customer.name = response_body["name"]
    customer.postal_code = response_body["postal_code"]
    customer.phone = response_body["phone"]
    #customer.registered_at = response_body["registered_at"]
    #customer.videos_checked_out_count = response_body["videos_checked_out_count"]
    db.session.commit()
    return jsonify(customer.to_json()), 200

@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
@customer_not_found
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"details":"customer successfully deleted",
                    "id": customer.id,
                    "name": customer.name}), 200


#---------------------# VIDEO ENDPOINTS #---------------------#

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def videos_index():
    videos = Video.query.all()
    videos_response = [video.to_json() for video in videos]
    return jsonify(videos_response), 200

@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
@video_not_found
def single_video(video_id):
    video = Video.query.get(video_id)
    return jsonify(video.to_json()), 200

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_video():
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return jsonify({"details": "Invalid Data"}), 400
    new_video = Video(title = request_body["title"],
                    release_date = request_body["release_date"],
                    total_inventory = request_body["total_inventory"],
                    #making available_inventory = to total because it's a brand new movie
                    available_inventory = request_body["total_inventory"])
    db.session.add(new_video)
    db.session.commit()
    return jsonify(new_video.to_json()), 201

@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
@video_not_found
def update_video(video_id):
    video = Video.query.get(video_id)
    response_body = request.get_json()
    if "title" not in response_body or "release_date" not in response_body or "total_inventory" not in response_body:
            return jsonify({"details": "Invalid Data"}), 400
    video.title = response_body["title"]
    video.release_date = response_body["release_date"]
    video.total_inventory = response_body["total_inventory"]
    db.session.commit()
    return jsonify(video.to_json()), 200

@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
@video_not_found
def delete_video(video_id):
    video = Video.query.get(video_id)
    db.session.delete(video)
    db.session.commit()
    return jsonify({"details":"video successfully deleted",
                    "id": video.id,
                    "title": video.title}), 200
