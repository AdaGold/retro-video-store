from flask import Blueprint, request, make_response
from app.models.customer import Customer
from app.models.video import Video
from app import db
import requests
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
@customers_bp.route("", methods= ["GET", "POST"])
def handle_get_customers():
    if request.method == "GET":
        customers = Customer.query.all()
        get_response =[]
        for customer in customers:
            get_response.append(customer.make_json)

        return get_response
    
    elif request.method == "POST":
        request_body = request.get_json()

        if "name" not in request_body.keys() \
            or "postal_code" not in request_body.keys() \
                or "phone" not in request_body.keys():
                return make_response({"details": "Invalid data"}, 400) 
        
        new_customer = Customer(name=request_body["name"],\
            postal_code=request_body["postal_code"], phone=request_body["phone"])
        
        db.session.add(new_customer)
        db.session.commit()
        return make_response(new_customer.make_json, 201)

@customers_bp.route("/<id>", methods = ["GET", "PUT", "DELETE"])
def handle_customer(id):
    customer = Customer.query.get(id)

    if customer is None:
        return make_response("", 404)

    elif request.method == "GET":
        return customer.make_json
    
    elif request.method == "PUT":
        request_body = request.get_json()

        if "name" not in request_body.keys() \
            or "postal_code" not in request_body.keys() \
                or "phone" not in request_body.keys():
                return make_response({"details": "Invalid data"}, 400) 
        
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
        return customer.make_json
    
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return {
            "details": \
                (f"Customer {customer.id} \"{customer.name}\" successfully deleted")
        }

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
@videos_bp.route("", methods= ["GET", "POST"])
def handle_videos():
    if request.method == "GET":
        videos = Video.query.all()
        get_response =[]
        for video in videos:
            get_response.append(video.make_json)

        return get_response
    
    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body.keys()\
            or "release_date" not in request_body.keys() \
                or "total_inventory" not in request_body.keys() \
                    or not isinstance(request_body["total_inventory"], int):
                return make_response({"details": "Invalid data"}, 400) 
        
        new_video = Video(title=request_body["title"],\
            release_date=request_body["release_date"], total_copies=request_body["total_inventory"])
        
        db.session.add(new_video)
        db.session.commit()
        return make_response(new_video.make_json, 201)

@videos_bp.route("/<id>", methods = ["GET", "PUT", "DELETE"])
def handle_video(id):
    video = Video.query.get(id)

    if video is None:
        return make_response("", 404)

    elif request.method == "GET":
        return video.make_json
    
    elif request.method == "PUT":
        request_body = request.get_json()

        if "title" not in request_body.keys() \
            or "release_date" not in request_body.keys() \
                or "total_inventory" not in request_body.keys() \
                    or not isinstance(request_body["total_inventory"], int):
                return make_response({"details": "Invalid data"}, 400) 
        
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_copies = request_body["total_inventory"]
        return video.make_json
    
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return {
            "details": \
                (f"Video {video.id} \"{video.name}\" successfully deleted")
        }