from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime, date, time, timezone
from dotenv import load_dotenv
import os
import requests
import json

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers_index():
    
    customers = Customer.query.all()
    customers_response = []
    
    if customers is None:
        return jsonify(customers_response), 200

    else:
        for customer in customers:
            customers_response.append({
                "id": customer.customer_id,
                "name": customer.name,
                "registered_at": customer.register_at,
                "postal_code": customer.postal_code,
                "phone": customer.phone,
                "videos_checked_out_count": 0
            })
        return jsonify(customers_response), 200


@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def handle_single_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(f"customer {customer_id} doesn't exist."), 404
    
    else:
        return jsonify({"id": customer.customer_id,
                    "name": customer.name,
                    "registered_at": customer.register_at,
                    "postal_code": customer.postal_code,
                    "phone": customer.phone,
                    "videos_checked_out_count": 0
                }), 200


@customers_bp.route("", methods=["POST"], strict_slashes=False)
def handle_customers():
    request_body = request.get_json()

    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_customer = Customer(name= request_body["name"],
    postal_code= request_body["postal_code"],
    phone= request_body["phone"])

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"id": new_customer.customer_id}), 201


@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    request_body = request.get_json()
    
    if customer is None:
        return jsonify(f"customer {customer_id} doesn't exist."), 404
    
    elif "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    else:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]

        db.session.commit()

        return jsonify({"customer": {
            "id": customer.customer_id,
            "name": customer.name,
            "registered_at": customer.register_at,
            "postal_code": customer.postal_code,
            "phone": customer.phone,
            "videos_checked_out": 0}}), 200


@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    
    if customer is None:
        return jsonify(f"customer {customer_id} doesn't exist."), 404
    
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"id": customer.customer_id}), 200


@videos_bp.route("", methods=["GET"], strict_slashes=False)
def videos_index():
    
    videos = Video.query.all()
    videos_response = []
    
    if videos is None:
            return jsonify(videos_response), 200

    else:
        for video in videos:
            videos_response.append({
                "id": video.video_id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory": video.total_inventory,
                "available_inventory": 0})
        return jsonify(videos_response), 200


@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def handle_single_video(video_id):

    video = Video.query.get(video_id)
    
    if video is None:
        return jsonify(f"customer {video_id} doesn't exist."), 404
    
    return jsonify({
        "id": video.video_id,
        "title": video.title,
        "release_date": video.release_date,
        "total_inventory": video.total_inventory,
        "available_inventory": 0}), 200


@videos_bp.route("", methods=["POST"], strict_slashes=False)
def handle_videos():
    request_body = request.get_json()
    
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_video = Video(title= request_body["title"], 
        release_date= request_body["release_date"],
        total_inventory= request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit()

    return jsonify({"id": new_video.video_id,
        "title": new_video.title,
        "release_date": new_video.release_date,
        "total_inventory": new_video.total_inventory,
        "available_inventory": 0}), 201


@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_single_video(video_id):
    video = Video.query.get(video_id)
    request_body = request.get_json()

    if video is None:
        return jsonify(f"customer {video_id} doesn't exist."), 404
    
    elif "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    video.title = request_body["title"]
    video.release_date= request_body["release_date"]
    video.total_inventory= request_body["total_inventory"]

    db.session.commit()

    return jsonify({"id": video.video_id,
        "title": video.title,
        "release_date": video.release_date,
        "total_inventory": video.total_inventory,
        "available_inventory": 0}), 200


@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_video(video_id):
    video = Video.query.get(video_id)
    
    if video is None:
        return jsonify(f"customer {video_id} doesn't exist."), 404
    
    db.session.delete(video)
    db.session.commit()

    return jsonify({"id": video.video_id}), 200