from app import db
from app.models import video
from app.models import customer
from app.models.customer import Customer
from app.models.rentals import Rental
from app.models.video import Video
from flask import json, request, Blueprint, make_response, jsonify
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
import os
from dotenv import load_dotenv
import requests

load_dotenv()

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# CRUD CUSTOMERS
@customer_bp.route("", methods=["GET"])
def list_customers():
    """Retrieves all customers and their related data from database"""
    customers = Customer.query.all()

    list_of_customers = []
    if not customers:
        return jsonify(list_of_customers)
    for customer in customers: 
        list_of_customers.append(customer.to_json()) 
    return jsonify(list_of_customers)

@customer_bp.route("/<customer_id>", methods=["GET"])
def list_single_customer(customer_id):
    """Retrieves data of specific customer"""
    single_customer = Customer.query.get(customer_id)
    if not single_customer:
        return make_response({"details": f"There is no customer in the database with ID #{customer_id}"}, 404)
    single_customer.postal_code = int(single_customer.postal_code)

    return jsonify(single_customer.to_json())

@customer_bp.route("", methods=["POST"])
def create_customer():
    """Create a customer for the database"""
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response({"details": "Customer name, phone number and postal code must all be provided, and they must be strings"}, 400)
    new_customer = Customer(name=request_body["name"],
    postal_code=request_body["postal_code"],
    phone_number=request_body["phone"],
    register_at=datetime.now())

    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.customer_id}, 201)

@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_single_customer(customer_id):
    """Updates data of specific customer"""
    single_customer = Customer.query.get(customer_id)
    
    if not single_customer:
        return make_response({"details": f"Cannot perform this function. There is no customer in the database with ID #{customer_id}"}, 404)
    
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body: 
        return make_response({"details": "Customer name, phone number and postal code must all be provided."}, 400)
    elif (type(request_body["name"]) != str) or (type(request_body["postal_code"]) != int) or (type(request_body["phone"]) != str):
        return make_response({"details: Customer name and phone number must be strings. Postal code must be an integer."}, 400)
    single_customer.name = request_body["name"]
    single_customer.postal_code = request_body["postal_code"] 
    single_customer.phone_number = request_body["phone"]
    db.session.commit()
    return jsonify(single_customer.to_json())

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_single_customer(customer_id):
    """Delete a specific customer from the database"""
    single_customer = Customer.query.get(customer_id)
    if not single_customer:
        return make_response({"details": f"Cannot perform this function. There is no customer in the database with ID #{customer_id}"}, 404)

    db.session.delete(single_customer)
    db.session.commit()
    return make_response({"id": single_customer.customer_id}, 200)

# CRUD VIDEOS
@video_bp.route("", methods=["GET"])
def list_videos():
    """Retrieves all videos and their related data from database"""
    videos = Video.query.all()
    list_of_videos = []
    
    if not videos:
        return jsonify(list_of_videos)
    
    for video in videos:
        list_of_videos.append(video.to_json())
    return jsonify(list_of_videos)

@video_bp.route("/<video_id>", methods=["GET"])
def list_single_video(video_id):
    """Retrieves data of specific video"""
    single_video = Video.query.get(video_id)
    
    if not single_video:
        return make_response({"details": f"There is no video in the database with ID #{video_id}"}, 404)
    return jsonify(single_video.to_json())

@video_bp.route("", methods=["POST"])
def create_video():
    """Create a video for the database"""
    request_body = request.get_json()

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body: 
        return make_response({"details": "Video title, release date and total in inventory must all be provided, and they must be string, datetime and integer values, respectively."}, 400)

    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"],
                    available_inventory=request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit()
    return make_response({"id": new_video.video_id}, 201)

@video_bp.route("/<video_id>", methods=["PUT"])
def update_single_video(video_id):
    """Updates data of a specific video"""
    single_video = Video.query.get(video_id)
    if not single_video:
        return make_response({"details": f"Cannot perform this function. There is no video in the database with ID #{video_id}"}, 404)

    request_body = request.get_json()

    # convert str to datetime object
    request_body["release_date"] = datetime.fromisoformat(request_body["release_date"])

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body: 
        return make_response({"details": "Video title, release date and inventory counts must all be provided."}, 400)
    elif (type(request_body["title"]) != str) or (type(request_body["release_date"]) != datetime) or (type(request_body["total_inventory"]) != int): 
        return make_response({"details": "Video title must be a string, release date must be a datetime object and inventory/available counts must both be integers."}, 400)
    else:
        single_video.title = request_body["title"]
        single_video.release_date = request_body["release_date"]
        single_video.total_inventory = request_body["total_inventory"]

        db.session.commit()
        return jsonify(single_video.to_json())

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_single_video(video_id):
    """Delete a specific video from the database"""
    single_video = Video.query.get(video_id)
    
    if not single_video:
        return make_response({"details": f"Cannot perform this function. There is no video in the database with ID #{video_id}"}, 404)

    db.session.delete(single_video)
    db.session.commit()
    return make_response({"id": single_video.video_id}, 200) 

# CRUD RENTALS
@rental_bp.route("/check-out", methods=["POST"])
def check_out_video():
    """Check out a video to a customer"""
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response({"details": "Incomplete entry. Please include customer ID and video ID."}, 400)
    elif (type(request_body["customer_id"]) != int) or (type(request_body["video_id"]) != int):
        return make_response({"details": "Customer ID and video ID must be integers!"}, 400)
    loaned_video = Rental(customer_id=request_body["customer_id"],
                                video_id=request_body["video_id"],
                                check_out_date=datetime.now()) 
    customer = Customer.query.get(loaned_video.customer_id)
    video = Video.query.get(loaned_video.video_id)

    if customer is None or video is None: 
        return make_response({"details": "The customer and/or the video does not exist."}, 404)
    if video.available_inventory == 0:
        return make_response({"details": "All copies of this video are checked out."}, 400)

    customer.videos_checked_out_count += 1
    video.available_inventory -= 1

    db.session.add(loaned_video)
    db.session.commit()
    return jsonify(loaned_video.to_json())

@rental_bp.route("/check-in", methods=["POST"])
def check_in_video():
    """Checks a customer's video back in"""
    request_body = request.get_json() 

    for detail in ["customer_id", "video_id"]: 
        if not (detail in request_body):
            return make_response({}, 400)
    returned_video = Rental(customer_id=request_body["customer_id"],
                            video_id=request_body["video_id"])
    customer = Customer.query.get(returned_video.customer_id)
    video = Video.query.get(returned_video.video_id)

    if customer is None or video is None:
        return make_response({"details": "The customer and/or the video does not exist."}, 404)
    if (video.video_id != request_body["video_id"]) or (customer.customer_id != request_body["customer_id"]):
        return make_response("", 400)
    if video.available_inventory == video.total_inventory:
        return make_response({
            "customer_id": customer.customer_id,
            "video_id": video.video_id,
            "videos_checked_out_count": customer.videos_checked_out_count, 
            "available_inventory": video.available_inventory
            }, 400)

    customer.videos_checked_out_count -= 1 
    video.available_inventory += 1

    db.session.add(returned_video)
    db.session.commit()
    return jsonify({
            "customer_id": customer.customer_id,
            "video_id": video.video_id,
            "videos_checked_out_count": customer.videos_checked_out_count, 
            "available_inventory": video.available_inventory
            })

@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def list_customer_videos(customer_id):
    """Retrieves all videos a customer has checked out"""
    hold_whats_relevant = {} 
    hold_dictified_entities = [] 
    customer_entity = [] 
    dictified_ce = {} 
    video_entity = [] 
    dictified_ve = {}
    rental_entity = []
    dictified_re = {}

    customer_vids = db.session.query(Customer, Video, Rental).join(Customer, Customer.customer_id==Rental.customer_id)\
        .join(Video, Video.video_id==Rental.video_id).filter(Customer.customer_id==customer_id).all()

    for tupled_entity in customer_vids: 
        if tupled_entity[0] == None:
            return make_response({"details": "Customer does not exist"}, 404)
        for entity in tupled_entity: 
            if type(entity) == Customer: 
                if entity.videos_checked_out_count == 0:
                    return jsonify([])
                customer_entity.append(entity)
                dictified_ce["id"] = entity.customer_id
                dictified_ce["name"] = entity.name
                dictified_ce["phone"] = entity.phone_number
                dictified_ce["postal_code"] = entity.postal_code
                dictified_ce["registered_at"] = entity.register_at
                dictified_ce["videos_checked_out_count"] = entity.videos_checked_out_count
                hold_dictified_entities.append(dictified_ce)
            elif type(entity) == Video:
                video_entity.append(entity)
                dictified_ve["id"] = entity.video_id 
                dictified_ve["title"] = entity.title
                dictified_ve["release_date"] = entity.release_date
                dictified_ve["total_inventory"] = entity.total_inventory
                dictified_ve["available_inventory"] = entity.available_inventory
                hold_dictified_entities.append(dictified_ve) 
            elif type(entity) == Rental:
                rental_entity.append(entity)
                dictified_re["customer_id"] = entity.customer_id 
                dictified_re["video_id"] = entity.video_id
                dictified_re["due_date"] = entity.check_out_date + (timedelta(days=7))
                dictified_re["videos_checked_out_count"] = entity.renter.videos_checked_out_count
                dictified_re["available_inventory"] = entity.video.available_inventory
                hold_dictified_entities.append(dictified_re)

    for dictified_entity in hold_dictified_entities: 
        if "release_date" in dictified_entity: 
            hold_whats_relevant["release_date"] = dictified_entity["release_date"]
        if "title" in dictified_entity:
            hold_whats_relevant["title"] = dictified_entity["title"]
        if "due_date" in dictified_entity:
            dictified_entity["due_date"] = str(dictified_entity["due_date"])
            hold_whats_relevant["due_date"] = dictified_entity["due_date"]
    return jsonify(hold_whats_relevant)

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def list_video_renters(video_id):
    """List the customers who currently have the video checked out"""
    hold_whats_relevant = {}
    hold_dictified_entities = []
    customer_entity = []
    dictified_ce = {}
    video_entity = []
    dictified_ve = {}
    rental_entity = []
    dictified_re = {}

    videos_by_customer = db.session.query(Video, Customer, Rental).join(Video, Video.video_id==Rental.video_id)\
        .join(Customer, Customer.customer_id==Rental.customer_id).filter(Video.video_id==video_id).all()

    for tupled_entity in videos_by_customer:
        if tupled_entity[0] == None:
            return make_response({"details": "Video does not exist"}, 404)
        for entity in tupled_entity:
            if type(entity) == Video:
                if entity.total_inventory == entity.available_inventory:
                    return jsonify([])
                video_entity.append(entity) 
                dictified_ve["id"] = entity.video_id 
                dictified_ve["title"] = entity.title
                dictified_ve["release_date"] = entity.release_date
                dictified_ve["total_inventory"] = entity.total_inventory
                dictified_ve["available_inventory"] = entity.available_inventory
                hold_dictified_entities.append(dictified_ve)
            elif type(entity) == Customer: 
                customer_entity.append(entity)
                dictified_ce["id"] = entity.customer_id 
                dictified_ce["name"] = entity.name
                dictified_ce["phone"] = entity.phone_number
                dictified_ce["postal_code"] = entity.postal_code
                dictified_ce["registered_at"] = entity.register_at
                dictified_ce["videos_checked_out_count"] = entity.videos_checked_out_count
                hold_dictified_entities.append(dictified_ce) 
            elif type(entity) == Rental:
                rental_entity.append(entity)
                dictified_re["customer_id"] = entity.customer_id 
                dictified_re["video_id"] = entity.video_id
                dictified_re["due_date"] = entity.check_out_date + (timedelta(days=7))
                dictified_re["videos_checked_out_count"] = entity.renter.videos_checked_out_count
                dictified_re["available_inventory"] = entity.video.available_inventory
                hold_dictified_entities.append(dictified_re)

    for dictified_entity in hold_dictified_entities: 
        if "name" in dictified_entity:
            hold_whats_relevant["name"] = dictified_entity["name"]
        elif "postal_code" in dictified_entity: 
            hold_whats_relevant["postal_code"] = dictified_entity["postal_code"]
        elif "phone" in dictified_entity:
            hold_whats_relevant["phone"] = dictified_entity["phone"]
        elif "due_date" in dictified_entity:
            dictified_entity["due_date"] = str(dictified_entity["due_date"])
            hold_whats_relevant["due_date"] = dictified_entity["due_date"]
    return jsonify(hold_whats_relevant)


