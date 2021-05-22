from flask import Blueprint, request, jsonify, make_response
from app import db
from .models.customer import Customer
from .models.video import Video
from .models.rentals import Rental
from datetime import datetime, timedelta
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


#---------------------# HELPER FUNCS + DECORATORS #---------------------#

def invalid_input():
    return jsonify({"details":"Invalid data"}), 400

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
            return invalid_input()
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
            return invalid_input()
    customer.name = response_body["name"]
    customer.postal_code = response_body["postal_code"]
    customer.phone = response_body["phone"]
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

@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
@customer_not_found
def get_customer_rentals(customer_id):
    customer = Customer.query.get(customer_id)
    rentals = []
    for rental in customer.videos:
        video = Video.query.get(rental.video_id)
        dict = {
            "title": video.title,
            "release_date": video.release_date,
            "due_date": rental.due_date}
        rentals.append(dict)
    return jsonify(rentals), 200


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
            return invalid_input()
    new_video = Video(title = request_body["title"],
                    release_date = request_body["release_date"],
                    total_inventory = request_body["total_inventory"],
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
            return invalid_input()
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

@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
@video_not_found
def get_video_rentals(video_id):
    video = Video.query.get(video_id)
    rentals = []
    for rental in video.customers:
        customer = Customer.query.get(rental.customer_id)
        dict = {
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code,
            "due_date": rental.due_date}
        rentals.append(dict)
    return jsonify(rentals), 200


#---------------------# RENTALS ENDPOINTS #---------------------#

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out_video():
    request_body = request.get_json()
    #could check for customer and video id in request body
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    if not isinstance(video_id, int) or not isinstance(customer_id, int):
        return invalid_input()
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer is None or video is None:
        return jsonify({"details": "customer or video not Found"}), 404
    if video.available_inventory == 0:
        return jsonify({"details": "Video out of stock"}), 400
    customer.videos_checked_out_count += 1
    video.available_inventory -= 1
    new_rental = Rental(customer_id = customer_id,
                    video_id = video_id,
                    due_date = datetime.now() + timedelta(7))
    db.session.add(new_rental)
    db.session.commit()
    return jsonify(new_rental.check_out_to_json()), 200

@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in_video():
    #query only the rental that matches customer and video id?
    rentals = Rental.query.all()
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    for rental in rentals:
        if rental.customer_id == customer_id and rental.video_id == video_id and rental.check_in_date == None:
            rental.customer.videos_checked_out_count -= 1
            rental.video.available_inventory += 1
            rental.check_in_date = datetime.now()
            db.session.commit()
            return jsonify(rental.check_in_to_json()), 200
    return invalid_input()


#---------------------# OPTIONAL ENDPOINTS #---------------------#

@rentals_bp.route("/overdue", methods=["GET"], strict_slashes=False)
def overdue_rentals_index():
    rentals = Rental.query.all()
    overdue_rentals = [rental.overdue_to_json() for rental in rentals if rental.due_date < datetime.now() and rental.check_in_date == None]
    return jsonify(overdue_rentals), 200

@videos_bp.route("/<video_id>/history", methods=["GET"], strict_slashes=False)
@video_not_found
def video_history(video_id):
    video = Video.query.get(video_id)
    rentals = video.customers
    video_history = []
    for rental in rentals:
        if rental.due_date < datetime.now():
            video_history.append(rental.video_history_to_json())
    return jsonify(video_history), 200