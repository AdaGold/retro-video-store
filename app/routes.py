from app import db
from app.models.customer import Customer
from flask import Blueprint, request, make_response, jsonify
from datetime import datetime, timedelta
import requests
import os
from app.models.video import Video
from app.models.rental import Rental
import flask_migrate 

customer_bp = Blueprint("customer", __name__, url_prefix = "/customers")
video_bp = Blueprint("video", __name__, url_prefix = "/videos")
rental_bp = Blueprint("rental", __name__, url_prefix = "/rentals")

# --------------------------CUSTOMER ENDPOINTS--------------------------------

@customer_bp.route("", methods = ["GET"])
def get_all_customers():
    customers = Customer.query.all()
    all_customers = []
    for customer in customers:
        all_customers.append(customer.to_json())
    
    return jsonify(all_customers), 200


@customer_bp.route("/<id>", methods = ["GET"])
def customer_by_id(id):
    customer = Customer.query.get(id)
    if customer == None:
        return jsonify({"details": "customer not found"}), 404

    else:
        return jsonify(customer.to_json()), 200

@customer_bp.route("/<id>", methods = ["PUT"])
def update_customer(id):
    customer = Customer.query.get(id)
    request_body = request.get_json()
    if customer == None:
        return jsonify({"details": "customer not found"}), 404

    else:
        errors = ""
        information = ["name", "postal_code", "phone"]
        for info in information:
            if info not in request_body:
                errors = errors + info 
                if errors != "":
                    return jsonify({"details": errors}), 400

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone_number = request_body["phone"]

    db.session.commit()
    # print(jsonify(customer.to_json())), 200
    return jsonify(customer.to_json()), 200


@customer_bp.route("", methods = ["POST"])
def create_customer():
    request_body = request.get_json()
    errors = ""
    information = ["name", "postal_code", "phone"]
    for info in information:
        if info not in request_body:
            # add a string to the error message that says info field not found
            errors = errors + info 
    # at the end of our loop, if the errors variable != ""
            if errors != "":
    # return a jsonified response where we use error string as value for key "details"
                return jsonify({"details": errors}), 400

    else:
        new_customer = Customer(name = request_body["name"],
                postal_code = request_body["postal_code"],
                phone_number = request_body["phone"])

    db.session.add(new_customer)
    db.session.commit()

    return jsonify(new_customer.to_json()), 201


@customer_bp.route("/<id>", methods = ["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer == None:
        return jsonify({"details": "customer not found"}), 404

    else: 
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"id": customer.id})

# -----------------------------VIDEO ENDPOINTS------------------------------

@video_bp.route("", methods = ["GET"])
def get_all_videos():
    videos = Video.query.all()
    all_videos = []
    for video in videos:
        all_videos.append(video.to_json())
    
    return jsonify(all_videos), 200


@video_bp.route("/<id>", methods = ["GET"])
def video_by_id(id):
    video = Video.query.get(id)
    if video == None:
        return jsonify({"details": "video not found"}), 404

    else:
        return jsonify({
            "id": video.id,
            "title": video.title,
            "release_date": video.release_date,
            "total_inventory": video.total_inventory
        }), 200


@video_bp.route("", methods = ["POST"])
def create_video():
    request_body = request.get_json()
    errors = ""
    information = ["title", "release_date", "total_inventory"]
    for info in information:
        if info not in request_body:
            errors = errors + info 
            if errors != "":
                return jsonify({"details": errors}), 400
    

    else:
        new_video = Video(title = request_body["title"],
            release_date = request_body["release_date"],
            total_inventory = request_body["total_inventory"],
            available_inventory = request_body["total_inventory"])

        db.session.add(new_video)
        db.session.commit()

        return jsonify({"id": new_video.id}), 201

@video_bp.route("/<id>", methods = ["PUT"])
def update_video(id):
    video = Video.query.get(id)
    request_body = request.get_json()
    if video == None:
        return jsonify({"details": "video not found"}), 404

    else:
        errors = ""
        information = ["title", "release_date", "total_inventory"]
        for info in information:
            if info not in request_body:
                errors = errors + info 
                if errors != "":
                    return jsonify({"details": errors}), 400

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.commit()
    return jsonify({
        "id": video.id,
        "title": video.title,
        "release_date": video.release_date,
        "total_inventory": video.total_inventory
    }), 200

@video_bp.route("/<id>", methods = ["DELETE"])
def delete_video(id):
    video = Video.query.get(id)
    if video == None:
        return jsonify({"details": "video not found"}), 404

    else: 
        db.session.delete(video)
        db.session.commit()
        return jsonify({"id": video.id})

# -----------------------------RENTAL ENDPOINTS-----------------------------

@rental_bp.route("/check-out", methods = ["POST"])
def rental_check_out():
    request_body = request.get_json()

    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")
    
    if type(customer_id) != int or type(video_id) != int:
        return jsonify({"details": "Invalid data"}), 400

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer is None and video is None:
        return jsonify({"details": "id's do not exist"}), 404

    if video.available_inventory < 1:
        return jsonify({"details": "2Invalid data"}), 400


    customer.videos_checked_out_count += 1
    video.available_inventory -= 1

    new_rental = Rental(
        customer_id = customer_id,
        video_id = video_id,
        due_date = datetime.now() + timedelta(days = 7)
    )

    db.session.add(new_rental)
    db.session.commit()

    return jsonify({
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }), 200


@rental_bp.route("/check-in", methods = ["POST"])
def rental_check_in():
    request_body = request.get_json()

    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")
    
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

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

    else:
        return jsonify({"details": "Invalid data"}), 400

@customer_bp.route("<int:id>/rentals", methods = ["GET"])
def customer_rentals(id):
    customer = Customer.query.get(id)

    if customer is None:
        return jsonify({"details": "customer not found"}), 404

    customer_rentals = []
    for rental in customer.video:
        video = Video.query.get(rental.video_id)
        customer_rentals.append({
            "release_date": video.release_date,
            "title": video.title,
            "due_date": datetime.now()+timedelta(days=7),
        })

    return jsonify(customer_rentals), 200

@video_bp.route("<int:id>/rentals", methods = ["GET"])
def video_rentals(id):
    video = Video.query.get(id)

    if video is None:
        return jsonify({"details": "video not found"}), 404

    video_rentals = []
    for rental in video.customer:
        customer = Customer.query.get(rental.customer_id)
        video_rentals.append({
            "due_date": datetime.now()+timedelta(days=7),
            "name": customer.name,
            "phone": customer.phone_number,
            "postal_code": customer.postal_code,
        })

        return jsonify(video_rentals), 200
