import re
from flask import Blueprint
from app import db
from .models.customer import Customer
from .models.video import Video
from flask import request, jsonify, make_response
from datetime import datetime
import requests

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

#Customer CRUD
@customer_bp.route("", methods = ["POST"], strict_slashes = False)
def create_customer():
    request_body = request.get_json()

    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response({"errors": ["Not Found"]}, 400)
    
    new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"],
                            register_at= datetime.now())
    
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.customer_id}, 201)

@customer_bp.route("", methods = ["GET"], strict_slashes = False)
def get_all_customers():
    customers = Customer.query.all()
    customer_list = []
    for customer in customers:
        customer_list.append(customer.to_json())
    
    return make_response(jsonify(customer_list))

@customer_bp.route("/<customer_id>", methods = ["GET"], strict_slashes = False)
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return make_response({"message": f"Customer {customer_id} Not Found"}, 404)
    return make_response(
        customer.to_json()
    , 200)

@customer_bp.route("/<customer_id>", methods = ["PUT"], strict_slashes = False)
def edit_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    form_data = request.get_json()
    if not customer:
        return make_response({"message": f"Customer {customer_id} Not Found"}, 404)
    if "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data:
        return make_response({"message": "Invalid data"}, 400)

    customer.name = form_data.get("name")
    customer.postal_code = form_data.get("postal_code")
    customer.phone = form_data.get("phone")
    #customer.register_at = form_data["registered_at"]

    db.session.commit()
    return make_response(customer.to_json(), 200)

@customer_bp.route("/<customer_id>", methods = ["DELETE"], strict_slashes = False)
def delete_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return make_response({"message": f"Customer {customer_id} was not found"}, 404)

    db.session.delete(customer)
    db.session.commit()
    return make_response({
        "id": int(customer_id)
    }, 200)

#Videos CRUD
@video_bp.route("", methods= ["POST", "GET"])
def handle_video():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response({"details": "Invalid data" }), 400
        
        new_video = Video(title=request_body["title"],release_date=request_body["release_date"],total_inventory=request_body["total_inventory"])
        
        db.session.add(new_video)
        db.session.commit()
        return make_response({
            "id": new_video.video_id
        }, 201)

    
    elif request.method == "GET":
        videos = Video.query.all()

        video_list = []
        for video in videos:
            video_list.append(video.to_json())
        return make_response(jsonify(video_list))

@video_bp.route("/<video_id>", methods = ["GET", "PUT", "DELETE"])
def deal_w_video(video_id):
    video = Video.query.get(video_id)

    if not video:
        return make_response({"message": f"Video {video_id} Not Found"}, 404)
    if request.method == "GET":
        return make_response(
            video.to_json()
        , 200)
    elif request.method == "PUT":
        form_data = request.get_json()
        if "title" not in form_data or "release_date" not in form_data or "total_inventory" not in form_data:
            return make_response({"message": "Invalid data"}, 400)
        video.title = form_data.get("title")
        video.release_date = form_data.get("release_date")
        video.total_inventory = form_data.get("total_inventory")
        db.session.commit()
        return make_response(
            video.to_json()
        , 200)
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return make_response({
        "id": int(video_id)
    }, 200)
