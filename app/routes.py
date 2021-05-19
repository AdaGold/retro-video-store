from app import db
from .models.video import Video
from .models.customer import Customer
from .models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
from sqlalchemy import desc, asc
import datetime
import calendar
import os
from dotenv import load_dotenv
import requests

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customer_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customer_list = []
    for customer in customers:
        customer_list.append(customer.cust_details())

    return jsonify(customer_list), 200

@customer_bp.route("", methods=["POST"])
def create_new_customer():
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return jsonify({"errors": "Invalid data"}), 400      
    else:
        new_customer = Customer(name = request_body["name"],
        registered_at = datetime.datetime.now(),
        postal_code = request_body["postal_code"],
        phone = request_body["phone"])
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"id": new_customer.customer_id}), 201

@customer_bp.route("/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return jsonify({"error": "Invalid data"}), 404
    else:
        return jsonify(customer.cust_details()), 200

@customer_bp.route("/<customer_id>", methods=["PUT"])
def put_by_customer_id(customer_id):
    customer = Customer.query.get(customer_id)
    form_data = request.get_json()
    #failing these tests?
    if customer == None:
        return jsonify({"errors": "Customer not found"}), 404
    elif form_data == {}:
        return jsonify({"errors": "Invalid data"}), 400
    else:
        customer.name = form_data['name']
        customer.postal_code = form_data['postal_code']
        customer.phone = form_data['phone']
        db.session.commit()
        return jsonify(customer.cust_details()), 200

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return jsonify({"errors": "Customer not found"}), 404
    else:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"id": customer.customer_id}), 200

@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    video_list = []
    for video in videos:
        video_list.append(video.vid_details())

    return jsonify(video_list), 200

@video_bp.route("", methods=["POST"])
def create_new_video():
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return jsonify({"errors": "Invalid data"}), 400      
    else:
        new_video = Video(title = request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"])
        db.session.add(new_video)
        db.session.commit()

        return jsonify({"id": new_video.video_id}), 201

@video_bp.route("/<video_id>", methods=["GET"])
def get_video_by_id(video_id):
    video = Video.query.get(video_id)
    if video == None:
        return jsonify({"error": "Invalid data"}), 404
    else:
        return jsonify(video.vid_details()), 200

@video_bp.route("/<video_id>", methods=["PUT"])
def put_by_video_id(video_id):
    video = Video.query.get(video_id)
    form_data = request.get_json()
    if video == None:
        return jsonify({"errors": "Video not found"}), 404
    elif form_data == {}:
        return jsonify({"errors": "Invalid data"}), 400
    else:
        video.title = form_data['title']
        video.release_date = form_data['release_date']
        video.total_inventory = form_data['total_inventory']
        db.session.commit()
        return jsonify(video.vid_details()), 200

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video == None:
        return jsonify({"errors": "Video not found"}), 404
    else:
        db.session.delete(video)
        db.session.commit()
        return jsonify({"id": video.video_id}), 200