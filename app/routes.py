import re
from app import db
from flask import Blueprint, request, jsonify, make_response
from .models.customer import Customer
from .models.video import Video
from .models.rental import Rental
from datetime import datetime
import requests
import os

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")
video_bp = Blueprint("video", __name__, url_prefix="/videos")
rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

@customer_bp.route("",methods=["POST"],strict_slashes=False)
def create_customer():
    """
        Input: request to create a new instance of Customer  
        Output: error if required attributes are missing, python dict with id key 
                and value, or list of dicts of all queries in Customer database
    """
    request_body = request.get_json()
    if 'name' not in request_body:
        return make_response(jsonify({"error":"missing customer name"}), 400)
    if 'phone' not in request_body:
        return make_response(jsonify({"error":"missing phone number"}), 400)
    if 'postal_code' not in request_body:
        return make_response(jsonify({"error":"missing postal code"}), 400)
    
    else:
        new_customer = Customer(
            name = request_body['name'],
            postal_code = request_body['postal_code'],
            phone = request_body['phone']
            )
        
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"id":new_customer.id}), 201
    
    
@customer_bp.route("",methods=["GET"],strict_slashes=False)    
def get_customers():
    """
        Input: query to get all instances of customer from DB
        Output: list of dicts of all queries in database
    """
    customers = Customer.query.all()
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_python_dict())
    return jsonify(customer_response), 200

        
@customer_bp.route("/<id>",methods=["GET"],strict_slashes=False)
def get_customer(id):
    """
        Input: request to read a customer by id
        Output: 404 if the customer does not exist, dictionary of updated customer
    """
    customer = Customer.query.get(id)
    if not customer:
        return jsonify(message="customer id not found"), 404
    if not isinstance(customer.id,int):
        return jsonify(message="customer id must be integer"), 404
    return jsonify(customer.to_python_dict()), 200


@customer_bp.route("/<id>",methods=["PUT"],strict_slashes=False)
def update_customer(id):   
    """
        Input: request to update a customer by id
        Output: 404 if the customer does not exist or dictionary of updated customer
    """
    customer = Customer.query.get(id)
    if not customer:
        return jsonify(message="customer id not found"), 404
    
    request_body = request.get_json()
    if not request_body:
        return jsonify(message="bad request"), 400
    if "name" in request_body:
        customer.name = request_body['name']
    if "postal_code" in request_body:
        customer.postal_code = request_body['postal_code']
    if "phone" in request_body:
        customer.phone = request_body['phone']
    
    db.session.commit()
    return jsonify(customer.to_python_dict()), 200


@customer_bp.route("/<id>",methods=["DELETE"],strict_slashes=False)
def delete_customer(id):
    """
        Input: Request to delete a customer by id
        Output: 404 if the customer does not exist or dictionary of customer id deleted
    """
    customer = Customer.query.get(id)
    if not customer:
        return jsonify(message="customer id not found"), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"id": customer.id}), 200


@video_bp.route("",methods=["POST"],strict_slashes=False)
def create_video():
    """
        Input: request to create a new instance of Video or query for all instances  
        Output: error if required attrbutes are missing or python dict with id key and value
    """
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response(jsonify({"error":"missing title of video"}), 400)
    if "release_date" not in request_body:
        return make_response(jsonify({"error":"missing video release date"}), 400)
    if "total_inventory" not in request_body:
        return make_response(jsonify({"error":"missing video total inventory"}), 400)
    new_video = Video(
                title = request_body['title'],
                release_date = request_body['release_date'],
                total_inventory = request_body['total_inventory'],
                available_inventory = request_body['total_inventory']
            )
    db.session.add(new_video)
    db.session.commit()
    return jsonify({"id": new_video.id}), 201

@video_bp.route("",methods=["GET"],strict_slashes=False)
def get_videos():
    """
        Input: request to query all instances of Video  
        Output: list  of dictionaries of all queries in Video database      
    """    
    videos = Video.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_python_dict())
    return jsonify(videos_response), 200

@video_bp.route("/<id>",methods=["GET"],strict_slashes=False)
def get_video(id):
    """
        Input: request to read a video by id
        Output: 404 if the video does not exist, dictionary of updated video, or id of
                deleted video id
    """
    video = Video.query.get(id)
    if not video:
        return jsonify(errors=["video id not found"]), 404
    return jsonify(video.to_python_dict()), 200


@video_bp.route("/<id>",methods=["PUT"],strict_slashes=False)
def update_video(id):
    """
        Input: request to update a video by id
        Output: 404 if the video does not exist, dictionary of updated video
    """    
    video = Video.query.get(id)
    if not video:
        return jsonify(errors=["video id not found"]), 404
    request_body = request.get_json()
    video.title = request_body['title']
    video.release_date = request_body['release_date']
    video.total_inventory  = request_body['total_inventory']
    db.session.commit()
    return jsonify(video.to_python_dict()), 200


@video_bp.route("/<id>",methods=["DELETE"],strict_slashes=False)
def delete_video(id):
    """
        Input: request to delete a video by id
        Output: 404 if the video does not exist, dictionary with id of deleted video 
    """            
    video = Video.query.get(id)
    if not video:
        return jsonify(errors=["video id not found"]), 404
    db.session.delete(video)
    db.session.commit()
    return jsonify(id=int(id)), 200



@rental_bp.route("/check-out", methods=["POST"],strict_slashes=False)#Checks out a video to a customer, and updates the db data
def check_out():
    """
        Input:  request to make a new instance of Rental, valid customer_id video_id are required body params
        Output: python dictionary of new Rental instance 

    """
    request_body = request.get_json()
    if "customer_id" not in request_body:
        return  400
    if "video_id" not in request_body:
        return  400
    if not isinstance(request_body["video_id"],int) or request_body['video_id'] == None:#validating datatype in request
        return jsonify(error="video id must be an integer"), 400
    
    if not isinstance(request_body["customer_id"],int) or request_body['customer_id'] == None: #validating datatype in request
        return jsonify(error="video id must be an integer"), 400
    
    customer_id = request_body["customer_id"]#setting variables that will be used when Rental class method checkout is called
    video_id = request_body["video_id"]#setting variables that will be used when Rental class method checkout is called
    video = Video.query.get(video_id)
    if not video:
        return jsonify(details= "doesnt exist"), 400
    if video.available_inventory <= 0:
        return jsonify(details="video not available"), 400
    new_rental = Rental.checkout(customer_id, video_id)
    return jsonify(new_rental.to_python_dict()), 200


@rental_bp.route("/check-in", methods=['POST'],strict_slashes=False)#Checks in a video to a customer, and updates the db data
def check_in():
    """
        Input:  request to edit instance of Rental, customer_id video_id are required body params
        Output: python dictionary of new Rental instance 
    """
    request_body = request.get_json()
    if "customer_id" not in request_body:
        return  400
    if "video_id" not in request_body:
        return  400
    if not isinstance(request_body["video_id"],int) or request_body['video_id'] == None: 
        return jsonify(error="video id must be an integer"), 400
    if not isinstance(request_body["customer_id"],int) or request_body['customer_id'] == None: 
        return jsonify(error="customer id must be an integer"), 400
    
    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])
    rental = Rental.query.filter_by(video_id=video.id, customer_id=customer.id).first()
    if not rental:
        return jsonify(error="video id and customer id have no relationship"), 400
    db.session.delete(rental)#successful check-in, delete instance of Rental
    customer.decrease_checkout_count()
    video.increase_inventory()
    db.session.commit()
    
    return jsonify(
        {
        "customer_id": customer.id,
        "video_id": video.id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory 
    }
    ), 200


@customer_bp.route("/<id>/rentals",methods=["GET"],strict_slashes=False)#List the videos a customer currently has checked out
def videos_of_customer(id):
    """
        Input:  Request to read a list of videos by customer id 
        Output: Returns error if no match is found, returns list of dicts of videos checkout out to one customer
    """
    customer = Customer.query.get(id)
    if not customer:
        return jsonify(error="no matches found"), 404
    video_list = []
    for rental in customer.rentals:#looping through rental attribute for customer instance and grabbing the video_ids. 
        video = Video.query.get(rental.video_id)#querying rental table for video_id that was found in customer.rental column
        video_dict = {
        "title" : video.title,
        "release_date" : video.release_date,
        "due_date": rental.due_date
        }
        video_list.append(video_dict)
    return jsonify(video_list), 200
        
         
@video_bp.route("/<id>/rentals",methods=["GET"],strict_slashes=False)#List the customers who currently have the video checked out
def customer_by_videos(id):
    """
        Input:  Request to read a list of customers who have a specific video checked out
        Output: Returns error if no match is found, returns list of dicts 
    """
    video = Video.query.get(id)
    if not video:
        return jsonify(error="no matches found"), 404
    checkout_list = []
    for rental in video.rentals:# list of rentals by attribute rentals in video
        customer = Customer.query.get(rental.customer_id)
        checkout = {
            "due_date": rental.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        }
        checkout_list.append(checkout)
    return jsonify(checkout_list), 200

