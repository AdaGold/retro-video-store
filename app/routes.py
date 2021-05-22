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

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_rentals_by_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    rental_list = []
    for rental in customer.rentals:
        video = Video.query.get_or_404(rental.video_id)
        rental_list.append({"release_date" : video.release_date,
            "title" : video.title,
            "due_date" : rental.due_date
            })

    return jsonify(rental_list),200

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
                available_inventory = request_body["total_inventory"],
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


@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def get_rentals_by_customer(video_id):
    video = Video.query.get_or_404(video_id)

    rental_list = []
    for rental in video.rentals:
        customer = Customer.query.get_or_404(rental.customer_id)
        rental_list.append({"name" : customer.name,
                            "phone" : customer.phone,
                            "postal_code" : customer.postal_code,
                            "due_date" : rental.due_date
                            })

    return jsonify(rental_list),200

# ==== Rentals ==== 

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out_rental():

    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if type(customer_id) is not int or type(video_id) is not int: 
        return {"details" : "Invalid data"}, 400

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer and video: 
        if video.available_inventory <= 0: 
            return {"details": "insufficient inventory"}, 400
        
        new_rental = Rental(customer_id=customer_id, video_id=video_id)

        customer.videos_checked_out_count += 1
        if video.available_inventory > 0:
            video.available_inventory -= 1

        db.session.add(new_rental)
        db.session.commit()
        return jsonify(new_rental.rental_to_json()), 200
    
    return make_response("", 404)


@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in_rental():
    
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    
    if type(customer_id) is not int or type(video_id) is not int: 
        return {"details": "Invalid data"}, 400

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer and video: 
        rental = Rental.query.filter_by(customer_id=customer_id, video_id=video_id).all()
        if rental: 
            customer.videos_checked_out_count -= 1
            video.available_inventory += 1

            for rental in rental:
                db.session.delete(rental)
            db.session.commit()

            to_json = rental.rental_to_json()
            del to_json["due_date"]
            return jsonify(to_json), 200

        return {"details": "this rental record does not exist"}, 400
    return make_response("", 404) 