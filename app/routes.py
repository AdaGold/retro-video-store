from app import db
from app.models.customer import Customer
from flask import Blueprint, request, make_response, jsonify
from datetime import datetime
import requests
import os
from app.models.video import Video
import flask_migrate 

customer_bp = Blueprint("customer", __name__, url_prefix = "/customers")
video_bp = Blueprint("video", __name__, url_prefix = "/videos")

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
        return (f"Customer not found"), 404

    else:
        return jsonify(customer.to_json()), 200

@customer_bp.route("/<id>", methods = ["PUT"])
def update_customer(id):
    customer = Customer.query.get(id)
    request_body = request.get_json()
    if customer == None:
        return (f"Customer not found"), 404

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
        return (f"Customer not found"), 404

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


@video_bp.route("/<video_id>", methods = ["GET"])
def video_by_id(video_id):
    video = Video.query.get(video_id)
    if video == None:
        return (f"Video not found"), 404

    else:
        return jsonify(video.to_json()), 200


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
                total_inventory = request_body["total_inventory"])

        db.session.add(new_video)
        db.session.commit()

        return jsonify(new_video.to_json()), 201

@video_bp.route("/<video_id>", methods = ["PUT"])
def update_video(video_id):
    video = Video.query.get(video_id)
    request_body = request.get_json()
    if video == None:
        return (f"Video not found"), 404

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
    return jsonify(video.to_json()), 200

@video_bp.route("/<video_id>", methods = ["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video == None:
        return (f"Video not found"), 404

    else: 
        db.session.delete(video)
        db.session.commit()
        return jsonify({"id": video.video_id})
