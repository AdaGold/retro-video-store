from flask import Blueprint
from flask.signals import request_finished
from app import db
from flask import request, make_response, jsonify
from sqlalchemy import DateTime
from datetime import datetime, date, timedelta
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
import os
import requests

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# Wave 1 Customer routers
# Lists all existing customers and details about each customer. No arguments
@customer_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.customer_info())

    return jsonify(customers_response)


# Gives back details about specific customer with required argument "id"
@customer_bp.route("/<customer_id>", methods=["GET"])
def get_specific_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("", 404)
    else:
        return make_response(customer.customer_info(), 200)


# Creates a new video with the params "name", "postal_code", "phone"
@customer_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    required_properties = ["name", "postal_code", "phone"]
    for prop in required_properties:
        if prop not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        
    new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone_number=request_body["phone"])

    db.session.add(new_customer)
    db.session.commit() 
    
    return make_response({"id": new_customer.customer_id}, 201)


# Updates and returns details about specific customer with params "name", "postal_code", and "phone"
@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    customer_data = request.get_json()

    if customer is None:
        return make_response("", 404)

    if ("name" or "postal_code" or "phone") not in customer_data:
        return make_response({"details": "Invalid data"}, 400) 
    else:
        customer.name=customer_data["name"]
        customer.postal_code=customer_data["postal_code"]
        customer.phone_number=customer_data["phone"]
        
        db.session.commit()
        return make_response(customer.customer_info(), 200)


@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("", 404)
    else:
        db.session.delete(customer)
        db.session.commit()
        
        return make_response({"id": customer.customer_id}, 200)


# Wave 1 Video routes
@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.video_info())

    return jsonify(videos_response)


@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    required_properties = ["title", "release_date", "total_inventory"]
    for prop in required_properties:
        if prop not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        
    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit() 
    return make_response({"id": new_video.video_id}, 201)


@video_bp.route("/<video_id>", methods=["GET"])
def get_videos(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response("", 404)
    else:
        return make_response(video.video_info())


@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response("", 404)
    else:
        video_data = request.get_json()
        video.title = video_data["title"]
        video.release_date = video_data["release_date"]
        video.total_inventory = video_data["total_inventory"]
        
        db.session.commit()
        return make_response(video.video_info(), 200)
        

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    
    if video is None:
        return make_response("", 404)
    else:
        db.session.delete(video)
        db.session.commit()
        
        return make_response({"id": video.video_id}, 200)


# Wave 2 Rental routes
# Checks out a video to a customer, and updates the data in the database
"""
When successful, this request should:
    increase the customer's videos_checked_out_count by one
    decrease the video's available_inventory by one
    create a due date. The rental's due date is the seven days from the current date.
"""
@rental_bp.route("/rentals/check-out", methods=["POST"])
def rental_checkout(customer_id, video_id):
    rental = Rental.query.all(customer_id, video_id)
    rental_data = request.get_json()

    if "customer_id" or "video_id" not in rental_data:
        return make_response({"details": "Invalid data"}, 404) 
        
    if "available_inventory" < 1 in rental_data:
        return make_response({"details": "Invalid data"}, 404)
        
    # checked_out_rental = Rental(customer_id=rental_data["customer_id"],
    #                         video_id=rental_data["video_id"],
    #                         due_date=rental_data["due_date"],
    #                         videos_checked_out_count=rental_data["videos_checked_out_count"],
    #                         available_inventory=rental_data["available_inventory"])

    # db.session.add(checked_out_rental)
    # db.session.commit() 
    
    # return make_response(checked_out_rental.rental_info(), 200)


@rental_bp.route("/rentals/check-in", methods=["POST"])
def rental_checkin(customer_id, video_id):
    rental = Rental.query.get(customer_id, video_id)
    rental_data = request.get_json()

    if "customer_id" or "video_id" not in rental_data:
        return make_response({"details": "Invalid data"}, 404) 
        
    if "customer_id" and "video_id" not in rental_data:
        return make_response({"details": "Invalid data"}, 404)
        
    # checked_in_rental = Rental(customer_id=rental_data["customer_id"],
    #                         video_id=rental_data["video_id"],
    #                         videos_checked_out_count=rental_data["videos_checked_out_count"],
    #                         available_inventory=rental_data["available_inventory"])

    # db.session.add(checked_in_rental)
    # db.session.commit() 
    
    # return make_response(checked_in_rental.rental_info(), 200)

# List the videos a customer currently has checked out
@rental_bp.route("customers/<customer_id>/rentals", methods=["GET"])
def customers_video_rentals(customer_id):
    rental = Rental.query.get(customer_id)
    rental_data = request.get_json()

    if rental is None:
        return make_response("", 404)
    # else:
    #     rental.release_date=rental_data["release_date"]
    #     rental.title=rental_data["title"]
    #     rental.due_date=rental_data["due_date"]

    #     return make_response(rental.rental_info(), 200)

# List the customers who currently have the video checked out
@rental_bp.route("videos/<video_id>/rentals", methods=["GET"])
def customers_renting_video(video_id):
    rental = Rental.query.get(video_id)
    rental_data = request.get_json()

    if rental is None:
        return make_response("", 404)
    # else:
    #     # rental.due_date=rental_data["due_date"]
    #     # rental.name=rental_data["name"]
    #     # rental.title=rental_data["title"]
    #     # rental.due_date=rental_data["due_date"]
        
    #     return make_response(rental.rental_info(), 200)


