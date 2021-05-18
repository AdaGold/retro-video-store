from flask import Blueprint
from app.models.Videos import Video 
from app.models.Customers import Customer
from flask import Blueprint, make_response, jsonify, request
from app import db 
from datetime import datetime
import requests 
import os 

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

def return_404():
    return make_response("Whatever you are looking for, we didn't find it.", 404)

def update_customer_from_json(body):
    pass


@customer_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_json())
    
    return jsonify(customer_response), 200

@customer_bp.route("", methods=["DELETE"])
def delete_all_customers():
    customers = Customer.query.all()
    for customer in customers:
        db.session.delete(customer)
    db.session.commit()

    return make_response("All of the customers in the database have been deleted.", 200)

@customer_bp.route("/<customer_id>", methods=["GET"])
def get_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return return_404()
    else:
        return make_response(customer.to_json(), 200)

@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return return_404()
    else:
        request_body = request.get_json()
        try:
            customer.customer_name = request_body["name"]
            customer.customer_zip = request_body["postal_code"]
            customer.customer_phone = request_body["phone"]
        
        except KeyError:
            return make_response({"That didn't work.": "Invalid data or format."}, 400)
        
        db.session.commit()

        return make_response(customer.to_json(), 201)




@customer_bp.route("", methods=["POST"])
def post_new_customer():
    request_body = request.get_json()
    try:
        new_customer = Customer(customer_name=request_body["name"], customer_zip=request_body["postal_code"], customer_phone=request_body["phone"], register_at=datetime.now())
    except KeyError:
        return make_response({"That didn't work.": "Invalid data or format."}, 400)
    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.to_json(), 201)


@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
    else:
        return return_404()

    return make_response(f"Customer {customer.customer_id} has been deleted.", 200)


@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    video_response = []
    for video in videos:
        video_response.append(video.to_json())
    return jsonify(video_response), 200

@video_bp.route("", methods=["POST"])
def create_new_video():
    request_body = request.get_json()
    try:
        new_video = Video(video_title=request_body["title"], release_date=request_body["release_date"], total_inventory=request_body["total_inventory"])

    except KeyError:
        return make_response({"That didn't work.": "Invalid data or format."}, 400)
    
    db.session.add(new_video)
    db.session.commit()

    return make_response(new_video.to_json(), 201)

@video_bp.route("/<video_id>", methods=["GET"])
def get_single_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return return_404()
    
    return make_response(video.to_json(), 200)

@video_bp.route("/<video_id>", methods=["PUT"])
def update_single_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return return_404()
    else:
        request_body = request.get_json()
        try:
            video.video_title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory= request_body["total_inventory"]
        
        except KeyError:
            return make_response({"That didn't work.": "Invalid data or format."}, 400)
        
        db.session.commit()

        return make_response(video.to_json(), 200)

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_single_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return return_404()

    db.session.delete(video)
    db.session.commit()
    return make_response(f"The video ID: {video.video_id} has been deleted. ", 200)

@video_bp.route("", methods=["DELETE"])
def delete_all_videos():
    videos = Video.query.all()
    for video in videos:
        db.session.delete(video)

    db.session.commit()

    return make_response("All of the videos in the database have been deleted.", 200)