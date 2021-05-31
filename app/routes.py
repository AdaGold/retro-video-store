from flask import Blueprint, json
from flask.signals import request_finished
from app import db
from flask import request, make_response, jsonify
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
    request_body = request.get_json()

    if customer is None:
        return make_response("Not Found", 404)

    required_properties = ["name", "postal_code", "phone"]
    for prop in required_properties:
        if len(prop)==0 or prop not in request_body:
            return make_response({"details": "Bad Request"}, 400)
    else:
        customer.name=request_body["name"]
        customer.postal_code=request_body["postal_code"]
        customer.phone_number=request_body["phone"]
        
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
                    total_inventory=request_body["total_inventory"],
                    available_inventory=request_body["total_inventory"])

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
    request_body = request.get_json(silent=False)

    if video is None:
        return make_response("", 404)
    else:
        video.title=request_body["title"]
        video.release_date=request_body["release_date"]
        video.total_inventory=request_body["total_inventory"]
        
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
# Required request body parameters are customer_id and video_id
@rental_bp.route("/check-out", methods=["POST"])
def rental_checkout():
    request_body = request.get_json()
    customer = request_body["customer_id"]
    video = request_body["video_id"]

    if "customer_id" not in request_body or "video_id" not in request_body
        return make_response({"details": "Not Found"}, 404)

    if not isinstance(customer_id, int) or not isinstance(video_id, int):
        return make_response({"details": "Not Found"}, 404)
    
    video = Video.query.get(video_id)
    if video.available_inventory < 1:
        return make_response({"details": "Bad Request"}, 400)
    
    customer.videos_checked_out_count += 1
    video.available_inventory -= 1
    # Create this as a person who is renting something new
    new_rental = Rental(customer_id=customer_id,
                        video_id=video_id,
                        due_date=(datetime.now() + timedelta(days=7)))

    db.session.add(new_rental)
    db.session.commit()
    
    return jsonify({
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }), 200


# Checks in a video to a customer, and updates the data in the database as such.
# Required request body parameters are customer_id and video_id
@rental_bp.route("/check-in", methods=["POST"])
def rental_checkin():
    request_body = request.get_json()
    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")

    if customer is None or video is None:
        return make_response({"details": "Not Found"}, 404)
    
    if not isinstance(customer_id, int) or not isinstance(video_id, int):
        return({"details": "Bad Request"}, 400)

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    rental = Rental.query.all()

    for rental in customer.video:
        if rental.video_id == video_id:
            customer.videos_checked_out_count -= 1
            video.available_inventory += 1

            db.session.delete(rental)
            db.session.commit()
            
            return jsonify({
                "customer_id": customer_id,
                "video_id": video_id,
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory
            }), 200

# List the videos a customer currently has checked out
# Required arguments is customer_id
# @rental_bp.route("customers/<customer_id>/rentals", methods=["GET"])
# def customers_video_rentals(customer_id):
#     rental = Rental.query.get(customer_id)
#     rental_data = request.get_json()

#     if rental is None:
#         return make_response("", 404)
    # else:
    #     rental.release_date=rental_data["release_date"]
    #     rental.title=rental_data["title"]
    #     rental.due_date=rental_data["due_date"]

    #     return make_response(rental.rental_info(), 200)

# List the customers who currently have the video checked out
# Required arguments is video_id
# @rental_bp.route("videos/<video_id>/rentals", methods=["GET"])
# def customers_renting_video(video_id):
#     rental = Rental.query.get(video_id)
#     rental_data = request.get_json()

#     if rental is None:
#         return make_response("", 404)
    # else:
    #     # rental.due_date=rental_data["due_date"]
    #     # rental.name=rental_data["name"]
    #     # rental.title=rental_data["title"]
    #     # rental.due_date=rental_data["due_date"]
        
    #     return make_response(rental.rental_info(), 200)


