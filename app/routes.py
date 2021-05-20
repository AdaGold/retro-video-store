from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
import datetime
import requests
import os
from dotenv import load_dotenv

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
@customers_bp.route("", methods = ["GET"])
def customer_index():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers: customers_response.append(customer.to_json())
    return make_response(jsonify(customers_response), 200)

@customers_bp.route("", methods = ["POST"])
def customers():
    try:
        response_body = request.get_json()
        new_customer = Customer(name=response_body["name"], 
                                postal_code=response_body["postal_code"],
                                phone=response_body["phone"])
        new_customer.registered_at = datetime.datetime.now()
        db.session.add(new_customer)
        db.session.commit()
        return make_response({"id": new_customer.id}, 201)
    except KeyError: 
        return make_response({"errors": {"name": ["can't be blank"], "postal_code": ["can't be blank"], "phone": ["can't be blank"]}}, 400)

@customers_bp.route("/<id>", methods = ["GET", "PUT", "DELETE"])
def handle_customers(id):
    customer = Customer.query.get(id)
    if customer is None: return make_response({"errors":["Not Found"]}, 404)
    if not isinstance(customer.videos_checked_out_count, int): 
        return make_response({"errors": {"videos_checked_out_count": ["is not a number"]}}, 400)
    elif request.method == "GET": return make_response(customer.to_json(), 200)
    elif request.method == "PUT": 
        try:
            form_data = request.get_json() 
            customer.name = form_data["name"]
            customer.postal_code = form_data["postal_code"]
            customer.phone = form_data["phone"]
            db.session.commit() 
            return make_response(customer.to_json(), 200)
        except KeyError:
            return make_response({"errors": {"name": ["can't be blank"], "postal_code": ["can't be blank"], "phone": ["can't be blank"]}}, 400)
    elif request.method == "DELETE": 
        db.session.delete(customer)
        db.session.commit()
        return make_response({"id": customer.id}, 200) 

# @customers_bp.route("/<id>/rentals", methods = ["GET"])
# def customer_rentals(id):
#     pass

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods = ["GET"])
def video_index():
    videos = Video.query.all() 
    videos_response = [] 
    for video in videos: 
        videos_response.append(video.to_json()) 
    return make_response(jsonify(videos_response), 200)

@videos_bp.route("", methods = ["POST"])
def videos(): 
    try: 
        response_body = request.get_json() 
        new_video = Video(title=response_body["title"], 
                        release_date=response_body["release_date"],
                        total_inventory=response_body["total_inventory"]) 
        db.session.add(new_video)
        db.session.commit() 
        return make_response({"id": new_video.id}, 201)
    except KeyError: 
        return make_response({"errors": {"title": ["can't be blank"], "release_date": ["can't be blank"], "total_inventory": ["can't be blank"]}}, 400)

@videos_bp.route("/<id>", methods = ["GET", "PUT", "DELETE"])
def handle_videos(id): 
    video = Video.query.get(id) 
    if video is None: return make_response({"errors":["Not Found"]}, 404) 
    if not isinstance(video.total_inventory, int): 
        return make_response({"errors": {"total_inventory": ["is not a number"]}}, 400) 
    elif request.method == "GET": return make_response(video.to_json(), 200) 
    elif request.method == "PUT": 
        try: 
            form_data = request.get_json() 
            video.title= form_data["title"] 
            video.release_date = form_data["release_date"] 
            video.total_inventory= form_data["total_inventory"] 
            db.session.commit() 
            return make_response(video.to_json(), 200) 
        except KeyError: return make_response({"errors": {"title": ["can't be blank"], "release_date": ["can't be blank"], "total_inventory": ["can't be blank"]}}, 400) 
        # try: # if isinstance(video.total_inventory, int): # return video.total_inventory # except TypeError: # return make_response({"errors": {"total_inventory": ["is not a number"]}}, 400)
    elif request.method == "DELETE": 
        db.session.delete(video) 
        db.session.commit() 
        return make_response({"id": video.id}, 200)

# @videos_bp.route("/<id>", methods = ["GET"])
# def video_rentals(id): 
#     pass