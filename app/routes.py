from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import asc, desc
from app import db
from app.models.customer import Customer
from app.models.video import Video 
from datetime import datetime
import requests
import os
import random


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


#=====================================================#
#                  CUSTOMER ROUTES                    #
#=====================================================#


@customers_bp.route("", methods=["GET"])
def get_list_all_customers():
    """
    Get all Customers in asc, desc, or unsorted order
    """
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        customers = Customer.query.order_by(asc("name"))
    elif sort_query == "desc":
        customers = Customer.query.order_by(desc("name"))
    else:
        customers = Customer.query.all()

    customers_response = [customer.to_json() for customer in customers]

    return jsonify(customers_response)


@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    """
    Get one Customer by id
    """
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("Customer not found", 404)

    customer_response = customer.to_json()
    return customer_response


@customers_bp.route("", methods=["POST"])
def add_new_customer():
    """
    Create a new Customer
    """
    request_body = request.get_json()

    try:
        request_body["name"]
        request_body["postal_code"]
        request_body["phone"]
    except:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    new_customer = Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"])

    db.session.add(new_customer)
    db.session.commit()

    return make_response({"id": new_customer.customer_id}, 201)


@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer_by_id(customer_id):
    """ 
    Update one Customer by id
    """
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("Customer not found", 404)

    request_body = request.get_json()
    try:
        request_body["name"]
        request_body["postal_code"]
        request_body["phone"]
    except:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()

    return make_response(customer.to_json(), 200)


@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id):
    """
    Delete one Customer by id
    """
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("Customer not found", 404)
    
    db.session.delete(customer)
    db.session.commit()

    return make_response({
        "id": customer_id
    })


#=====================================================#
#                     VIDEO ROUTES                    #
#=====================================================#


@videos_bp.route("", methods=["GET"])
def get_list_all_videoss():
    """
    Get all Videos in asc, desc, or unsorted order
    """
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        videos = Video.query.order_by(asc("name"))
    elif sort_query == "desc":
        videos = Video.query.order_by(desc("name"))
    else:
        videos = Video.query.all()

    videos_response = [video.to_json() for video in videos]

    return jsonify(videos_response)


@videos_bp.route("/<int:video_id>", methods=["GET"])
def get_video_by_id(video_id):
    """
    Get one Video by id
    """
    video = Video.query.get(video_id)

    if video is None:
        return make_response("Video not found", 404)

    video_response = video.to_json()
    return video_response

@videos_bp.route("", methods=["POST"])
def add_new_video():
    """
    Create a new Video
    """
    request_body = request.get_json()

    try:
        request_body["title"]
        request_body["release_date"]
        request_body["total_inventory"]
    except:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit()

    return make_response({"id": new_video.video_id}, 201)


@videos_bp.route("/<int:video_id>", methods=["PUT"])
def update_video_by_id(video_id):
    """ 
    Update one Video by id
    """
    video = Video.query.get(video_id)

    if video is None:
        return make_response("Video not found", 404)

    request_body = request.get_json()
    try:
        request_body["title"]
        request_body["release_date"]
        request_body["total_inventory"]
    except:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.commit()

    return make_response(video.to_json(), 200)


@videos_bp.route("/<int:video_id>", methods=["DELETE"])
def delete_video_by_id(video_id):
    """
    Delete one Video by id
    """
    video = Video.query.get(video_id)

    if video is None:
        return make_response("Video not found", 404)
    
    db.session.delete(video)
    db.session.commit()

    return make_response({
        "id": video_id
    })