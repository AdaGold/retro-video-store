from flask import Blueprint
from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime, timedelta
import os 
import requests 

#==== Customers ====#
customers_bp = Blueprint("customers",__name__,url_prefix="/customers")

@customers_bp.route("", methods=["GET","POST"])
def handle_customers():
    if request.method == "GET":
        customers = Customer.query.all()
        customers_list = []  
        for customer in customers:
            customers_list.append(customer.customer_to_json())
        return jsonify(customers_list), 200
    
    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_customer = Customer(
                name=request_body["name"],
                postal_code=request_body["postal_code"],
                phone=request_body["phone"])
        except KeyError:
            return make_response({"details" : "Invalid data"}, 400)
    
        db.session.add(new_customer)
        db.session.commit()
        return make_response(new_customer.customer_to_json(), 201)


@customers_bp.route("/<customer_id>", methods=["GET","PUT","DELETE"])
def handle_one_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == "GET":
        return jsonify(customer.customer_to_json()), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        try:
            customer.name = request_body["name"]
            customer.postal_code = request_body["postal_code"]
            customer.phone = request_body["phone"]
        except KeyError:
            return make_response({"details" : "Invalid data"}, 400)

        db.session.commit()
        return make_response(customer.customer_to_json(), 200)

    elif request.method == "DELETE":
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return ({"id" : int(customer_id)}, 200)


# ==== Videos ==== 
videos_bp = Blueprint("videos",__name__,url_prefix="/videos")

@videos_bp.route("", methods=["GET","POST"])
def handle_customers():
    if request.method == "GET":
        videos = Video.query.all()
        videos_list = []  
        for video in videos:
            videos_list.append(video.video_to_json())
        return jsonify(videos_list), 200
    
    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_video = Video(
                title=request_body["title"],
                release_date=request_body["release_date"],
                total_inventory=request_body["total_inventory"])
        except KeyError:
            return make_response({"details" : "Invalid data"}, 400)
    
        db.session.add(new_video)
        db.session.commit()
        return make_response(new_video.video_to_json(), 201)


@videos_bp.route("/<video_id>", methods=["GET","PUT","DELETE"])
def handle_one_video(video_id):
    video = Video.query.get_or_404(video_id)

    if request.method == "GET":
        return jsonify(video.video_to_json()), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        try:
            video.title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory = request_body["total_inventory"]
        except KeyError:
            return make_response({"details" : "Invalid data"}, 400)

        db.session.commit()
        return make_response(video.video_to_json(), 200)

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return ({"id" : int(video_id)}, 200)


#==== Rentals ==== 
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return None

@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video():
    check_out_data = request.get_json()
    if not is_int(check_out_data["customer_id"]) or not is_int(check_out_data["video_id"]):
        return {"details": "Invalid ID"}, 400

    customer = Customer.query.get_or_404(check_out_data["customer_id"])
    video = Video.query.get_or_404(check_out_data["video_id"])
    
    check_out_rental = Rental(**check_out_data)
    if video.available_inventory > 0:
        video.available_inventory -= 1
        customer.videos_checked_out_count += 1
        db.session.add(check_out_rental)
        db.session.commit()
        return check_out_rental.rental_to_json(), 200
    return {"details": "Inventory not available"}, 400

@rentals_bp.route("/check-in", methods=["POST"])
def check_in_video():
    check_in_data = request.get_json()
    if not is_int(check_in_data["customer_id"]) or not is_int(check_in_data["video_id"]):
        return {"details": "Invalid ID"}, 400

    check_in_rental = Rental.query.get_or_404((check_in_data["customer_id"], check_in_data["video_id"]))
    if check_in_rental.customer.videos_checked_out_count > 0:
        check_in_rental.video.available_inventory += 1
        check_in_rental.customer.videos_checked_out_count -= 1
        db.session.commit()
        response_body = check_in_rental.rental_to_json()
        del response_body["due_date"]
        return response_body, 200
    return {"details": "Rentals all returned"}, 400
