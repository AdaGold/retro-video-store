from re import I
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime, timedelta
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
        request_body = request.get_json()
        new_customer = Customer(name=request_body["name"], 
                                postal_code=request_body["postal_code"],
                                phone=request_body["phone"])
        new_customer.registered_at = datetime.now()
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

@customers_bp.route("/<id>/rentals", methods = ["GET"])
def customer_rentals(id):
    customer = Customer.query.get(id)
    if customer is None: return make_response({"errors":"Not Found"}, 404) 
    customer_rentals = Rental.query.filter_by(customer_id =customer.id)
    customer_videos = []

    for rental in customer_rentals:
        video=Video.query.get(rental.video_id)
        customer_videos.append({
                    "release_date": video.release_date,
                    "title": video.title,
                    "due_date": rental.due_date})
    return jsonify(customer_videos), 200



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
        request_body = request.get_json() 
        new_video = Video(title=request_body["title"], 
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"],
                        available_inventory=request_body["total_inventory"]) 
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
    elif request.method == "DELETE": 
        db.session.delete(video) 
        db.session.commit() 
        return make_response({"id": video.id}, 200)

@videos_bp.route("/<id>/rentals", methods = ["GET"])
def video_rentals(id): 
    video = Video.query.get(id)
    if video is None: 
        return make_response({"errors":"Not Found"}, 404) 
    video_rentals = Rental.query.filter_by(video_id = video.id)
    customers_by_video = []
    for rental in video_rentals:
        customer=Customer.query.get(rental.customer_id)
        
        customers_by_video.append({
                        "due_date": rental.due_date,
                        "name": customer.name,
                        "phone": customer.phone,
                        "postal_code": str(customer.postal_code)})
    return jsonify(customers_by_video), 200


rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods = ["POST"])
def check_out():
    request_body = request.get_json()
    customer_id = request_body.get("customer_id")
    video_id=request_body.get("video_id")

    if customer_id is None or video_id is None:
        return make_response({"errors": "Not Found"}, 404) 

    if not isinstance(customer_id, int) or not isinstance(video_id, int):
        return make_response({"errors": "Invalid data"}, 400)

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer is None or video is None: return make_response({"errors":"Not Found"}, 404) 

    if video.available_inventory == 0: return make_response({"errors": "No video available"}, 400)

    customer.videos_checked_out_count += 1
    video.available_inventory -= 1
    
    rental = Rental(customer_id = customer.id, video_id=video.id, due_date = datetime.now() + timedelta(days=7))
    db.session.add(rental)
    db.session.commit() 

    return {
        "customer_id": customer.id,
        "video_id": video.id,
        "due_date": rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
                }, 200


@rentals_bp.route("/check-in", methods = ["POST"])
def check_in():
    request_body = request.get_json()
    customer_id = request_body.get("customer_id")
    video_id=request_body.get("video_id")

    if customer_id is None or video_id is None:
        return make_response({"errors": "Not Found"}, 404) 
    if not isinstance(customer_id, int) or not isinstance(video_id, int):
        return make_response({"errors": "Invalid data"}, 400)

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    rental = Rental.query.filter_by(customer_id = customer_id, video_id = video_id).one_or_none()

    if customer is None or video is None or rental is None: 
        return make_response({"errors":"Not Found"}, 400) 


    customer.videos_checked_out_count -= 1
    video.available_inventory += 1
    db.session.delete(rental)
    db.session.commit()


    return jsonify({
        "customer_id": customer.id,
        "video_id": video.id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
        }), 200
