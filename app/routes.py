from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import jsonify
from flask import request, make_response
from datetime import datetime
import os
import requests 


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
#rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals") ### might not need this one


def bad_request():
    return ({"errors":["details here"]}, 400)

def no_customer_found(customer_id):
    return ({"errors":["Not Found"]}, 404)


@customers_bp.route("", methods=["GET"])
def get_customers_details():
    customers = Customer.query.all()
    customers_details = []
    for customer in customers:
        customers_details.append(customer.to_json())
    return jsonify(customers_details), 200


@customers_bp.route("", methods=["POST"])
def create_customers():
    request_body = request.get_json()
    if not "name" in request_body or not request_body.get("name"):
        return bad_request()
    if not "postal_code" in request_body or not request_body.get("postal_code"):
        return bad_request()
    if not "phone" in request_body or not request_body.get("phone"):
        return bad_request()
    new_customer = Customer(name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"])
    db.session.add(new_customer)
    db.session.commit()
    return ({"id":new_customer.id}, 201) 


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return make_response(customer.to_json(), 200)
    return no_customer_found(customer_id)


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        updated_info = request.get_json()
        if not "name" in updated_info or not updated_info.get("name"):
            return bad_request()
        if not "postal_code" in updated_info or not updated_info.get("postal_code"):
            return bad_request()
        if not "phone" in updated_info or not updated_info.get("phone"):
            return bad_request()
        customer.name = updated_info["name"]
        customer.postal_code = updated_info["postal_code"]
        customer.phone = updated_info["phone"]
        db.session.commit()
        return (customer.to_json(), 200)
    return no_customer_found(customer_id)


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return ({"id":int(customer_id)}, 200)
    return no_customer_found(customer_id)




def no_video_found(video_id):
    return ({"errors":["Not Found"]}, 404)

@videos_bp.route("", methods=["GET"])
def get_videos_details():
    videos = Video.query.all()
    videos_log = []
    for video in videos:
        videos_log.append(video.to_json())
    return jsonify(videos_log), 200


@videos_bp.route("", methods=["POST"])
def create_videos():
    request_body = request.get_json()
    if not "title" in request_body or not request_body.get("title"):
        return bad_request()
    if not "release_date" in request_body or not request_body.get("release_date"):
        return bad_request()
    if not "total_inventory" in request_body or not request_body.get("total_inventory"):
        return bad_request()
    new_video = Video(title=request_body["title"],
        release_date=request_body["release_date"],
    total_inventory=request_body["total_inventory"])
    db.session.add(new_video)
    db.session.commit()
    return ({"id":new_video.id}, 201) 


@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    video = Video.query.get(video_id)
    if video:
        return make_response(video.to_json(), 200) 
    return no_video_found(video_id)

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video = Video.query.get(video_id)
    if video:
        updated_info = request.get_json()
        if not "title" in updated_info or not updated_info.get("title"): 
            return bad_request()
        if not "release_date" in updated_info or not updated_info.get("release_date"):
            return bad_request()
        if not "total_inventory" in updated_info or not updated_info.get("total_inventory"):
            return bad_request()   
        video.title = updated_info["title"]
        video.release_date = updated_info["release_date"]
        video.total_inventory = updated_info["total_inventory"]
        db.session.commit()
        return make_response(video.to_json(), 200) 
    return no_video_found(video_id)


@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video:
        db.session.delete(video)
        db.session.commit()
        return {"id":int(video_id)}, 200
    return no_video_found(video_id)




