import datetime
from typing import ChainMap
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime
from dotenv import load_dotenv
import os
import requests

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")
customer_bp = Blueprint("customer_bp", __name__, url_prefix="/customers")
rental_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")

customer_keys = ["name", "phone", "postal_code"]

#Roslyn: Customer
@customer_bp.route("", methods=["GET"]) #Roslyn - I think we should break the functions up for each method
def read_customers():
    customer_response = []
    customers = sort_titles(request.args.get("sort"), Customer)
    customer_response = [customer.to_dict() for customer in customers]
    return jsonify(customer_response), 200

@customer_bp.route("", methods=["POST"]) #Roslyn - I think we should break the functions up for each method
def create_customer():
    request_body = request.get_json()
    is_complete = check_data(customer_keys, request_body)
    return is_complete if is_complete else create_customer(request_body)

@customer_bp.route("/<customer_id>", methods=["GET"])
def read_a_customer(customer_id):
    response = id_check(customer_id)
    if response:
        return response
    customer = Customer.query.get(customer_id)
    return not_found_response("Customer", customer_id) if not customer else make_response(customer.to_dict(),200)
    
@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_a_customer(customer_id):
    response = id_check(customer_id)
    if response:
        return response
    customer = Customer.query.get(customer_id)
    if not customer:
        return not_found_response("Customer", customer_id)
    db.session.delete(customer)
    db.session.commit()
    return make_response({"id": int(customer_id)}, 200)

@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_a_customer(customer_id):
    response = id_check(customer_id)
    if response:
        return response
    customer = Customer.query.get(customer_id)
    if not customer:
        return not_found_response("Customer", customer_id)
    request_body = request.get_json()
    is_complete = check_data(customer_keys, request_body)
    if is_complete:
        return is_complete
    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]
    db.session.commit()
    return make_response(customer.to_dict(), 200)

def create_customer(request_body):
        new_customer = Customer(name=request_body["name"],
                            phone=request_body["phone"], 
                            postal_code=request_body["postal_code"],
                            register_at=datetime.utcnow())
        db.session.add(new_customer)
        db.session.commit()
        return make_response(new_customer.to_dict(), 201)


def check_data(check_items, request_body): # Areeba - I think you could use this to check video "PUT" and "POST" request data too
    for key in check_items:
        if key not in request_body.keys():
            return make_response({"details": f"Request body must include {key}."}, 400)
    return False


def not_found_response(entity, id): # Areeba - you could use this and fill in "Video" as the "entity" parameter, or if you think this method is confusing or clunky, we can forego this function
    return make_response({"message" : f"{entity} {id} was not found"}, 404)

#----------------------------------------------------------------------------------#
#Areeba: Video 

video_keys = ["title", "release_date", "total_inventory"]

@video_bp.route("", methods=["GET"])
def read_videos():
    videos_response = []
    videos = sort_titles(request.args.get("sort"), Video)
    videos_response = [video.to_dict() for video in videos]
    return jsonify(videos_response), 200


@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    is_complete = check_data(video_keys, request_body)
    if is_complete:
        return is_complete
    else:
        new_video = Video(title=request_body["title"],
                            release_date=request_body["release_date"], 
                            total_inventory=request_body["total_inventory"])
        db.session.add(new_video)
        db.session.commit()
        return make_response(new_video.to_dict(), 201)

#These could be instance methods?
def sort_titles(sort_by, entity):
    #Thinking about making this a very generic function to sort anything with a simple order_by 
    if sort_by == "asc": 
        sorted = entity.query.order_by(entity.title.asc())
    elif sort_by == "desc":
        sorted = entity.query.order_by(entity.title.desc())
    else:
        sorted = entity.query.all()
    return sorted

def sort_dates(sort_by):
    #May want to use this for release_dates if sort_titles can't be made generic?
    pass 


@video_bp.route("/<video_id>", methods=["GET"])
def read_a_video(video_id):
    if not video_id.isnumeric():
        return make_response({"message" : "Please enter a valid video id"}, 400)
    video = Video.query.get(video_id)
    return not_found_response("Video", video_id) if not video else make_response(video.to_dict(),200)

def id_check(id):
    # DRYing code
    response = make_response({"message" : "Please enter a valid customer id"}, 400)
    return response if not id.isnumeric() else False


@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    if not video_id.isnumeric():
        return make_response({"message" : "Please enter a valid video id"}, 400)
    
    video = Video.query.get(video_id) 
    
    if not video:
        return not_found_response("Video", video_id)

    request_body = request.get_json()

    is_complete = check_data(video_keys, request_body)

    if is_complete:
        return is_complete
    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]
    db.session.commit()
    return make_response(video.to_dict(), 200)
    

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    if not video_id.isnumeric():
        return make_response({"message" : "Please enter a valid video id"}, 400)

    video = Video.query.get(video_id) 

    if not video:
        return not_found_response("Video", video_id)
    db.session.delete(video)
    db.session.commit()
    #return make_response({"id": int(video_id)}, 200)
    response = {"id": video.id}
    return make_response(response, 200)


#DRY for error checks: https://stackoverflow.com/questions/38488476/a-dry-approach-to-python-try-except-blocks