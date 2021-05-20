from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime
import requests

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods = ["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = []
    if customers is None:
        return make_response([])
    for customer in customers:
        customers_response.append({
            "id": customer.customer_id,
            "name": customer.name,
            "registered_at": customer.register_at,
            "postal_code": customer.postal_code,
            "phone": customer.phone_number,
            "videos_checked_out_count": 0
        })
    return jsonify(customers_response)

@customers_bp.route("/<customer_id>", methods = ["GET"])
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
            return make_response({"details": "Customer not found"}, 404)
    return {
            "id": customer.customer_id,
            "name": customer.name,
            "registered_at": customer.register_at,
            "postal_code": customer.postal_code,
            "phone": customer.phone_number,
            "videos_checked_out_count": 0
        }

@customers_bp.route("", methods = ["POST"])
def post_customers():
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    else:
        new_customer = Customer(name=request_body["name"], postal_code=request_body["postal_code"], phone_number=request_body["phone"])
        db.session.add(new_customer)
        db.session.commit()
        return make_response({
            "id": new_customer.customer_id,
            "name": new_customer.name,
            "postal_code": new_customer.postal_code,
            "phone": new_customer.phone_number,
        }, 201)

@customers_bp.route("/<customer_id>", methods = ["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response({"details": "Customer not found"}, 404)
    form_data = request.get_json()
    if "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data:
        return make_response({"details": "Invalid data"}, 400)
    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone_number = form_data["phone"]
    db.session.commit()
    return make_response(jsonify({
                        "id": customer.customer_id,
                        "name": customer.name,
                        "registered_at": customer.register_at,
                        "postal_code": customer.postal_code,
                        "phone": customer.phone_number,
                        "videos_checked_out_count": 0}))

@customers_bp.route("/<customer_id>", methods = ["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
            return make_response({"details": "Customer not found"}, 404)
    db.session.delete(customer)
    db.session.commit()
    return make_response(jsonify({"id": customer.customer_id})) 

@videos_bp.route("", methods = ["GET"])
def get_videos():
    videos = Video.query.all()
    videos_response = []
    if videos is None:
        return []
    for video in videos:
        videos_response.append({
            "id": video.video_id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory,
            "available_inventory": video.available_inventory
        })
    return jsonify(videos_response)

@videos_bp.route("/<video_id>", methods = ["GET"])
def get_one_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
            return make_response({"details": "Video not found"}, 404)
    return {
            "id": video.video_id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory,
            "available_inventory": video.available_inventory
        }

@videos_bp.route("", methods = ["POST"])
def post_videos():
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    else:
        new_video = Video(title=request_body["title"], release_date=request_body["release_date"], total_inventory=request_body["total_inventory"])
        db.session.add(new_video)
        db.session.commit()
        return make_response({
            "id": new_video.video_id
        }, 201)

@videos_bp.route("/<video_id>", methods = ["PUT"])
def update_videos(video_id):
    video = Video.query.get(video_id)
    if video is None:
            return make_response({"details": "Video not found"}, 404)
    form_data = request.get_json()
    if "title" not in form_data or "release_date" not in form_data or "total_inventory" not in form_data:
        return make_response({"details": "Invalid data"}, 400)
    else:
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]
        db.session.commit()
        return make_response(jsonify({
            "id": video.video_id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory,
            "available_inventory" : video.available_inventory }))

@videos_bp.route("/<video_id>", methods = ["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
            return make_response({"details": "Video not found"}, 404)
    else:
        db.session.delete(video)
        db.session.commit()
        return make_response(jsonify({"id": video.video_id})) 
