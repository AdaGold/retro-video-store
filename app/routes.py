from flask import request, Blueprint
from app import db
from flask import jsonify
from .models.customer import Customer
from .models.video import Video
import requests
import os

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")


@customer_bp.route("", methods=["POST"], strict_slashes=False)
def add_customer():
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return jsonify({
        "details": "Invalid data"
        }), 400
    new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"])
    
    db.session.add(new_customer)
    db.session.commit()
    return new_customer.to_json(), 201

@customer_bp.route("", methods=["GET"], strict_slashes=False)
def customer_index():
    customers = Customer.query.all()
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_json())

    return jsonify(customer_response), 200

@customer_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return jsonify(customer.to_json()), 200
    return "", 404

@customer_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        request_body = request.get_json()
        if "name" in request_body and "postal_code" in request_body and "phone" in request_body:
            customer.name = request_body["name"]
            customer.postal_code = request_body["postal_code"]
            customer.phone = request_body["phone"]
            db.session.commit()
            updated_customer = customer.to_json()
            return jsonify(updated_customer), 200
        return jsonify({
        "details": "Invalid data"
        }), 400
    return "", 404
  
@customer_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({
        "id": customer.customer_id
        }), 200
    return "", 404

@video_bp.route("", methods=["POST"], strict_slashes=False)
def add_video():
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return jsonify({
        "details": "Invalid data"
        }), 400
    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"])
    
    db.session.add(new_video)
    db.session.commit()
    return jsonify({
        "id": new_video.video_id
    }), 201

@video_bp.route("", methods=["GET"], strict_slashes=False)
def video_index():
    videos = Video.query.all()
    video_response = []
    for video in videos:
        video_response.append(video.to_json())

    return jsonify(video_response), 200

@video_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_video(video_id):
    video = Video.query.get(video_id)
    if video:
        return jsonify(video.to_json()), 200
    return "", 404

@video_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):
    video = Video.query.get(video_id)
    if video:
        request_body = request.get_json()
        if "title" in request_body and "release_date" in request_body and "total_inventory" in request_body:
            video.title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory = request_body["total_inventory"]
            db.session.commit()
            updated_video = video.to_json()
            return jsonify(updated_video), 200
        return jsonify({
        "details": "Invalid data"
        }), 400
    return "", 404

@video_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video:
        db.session.delete(video)
        db.session.commit()
        return jsonify({
        "id": video.video_id
        }), 200
    return "", 404