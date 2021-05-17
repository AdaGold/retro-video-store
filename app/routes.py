from app import db
from flask import Blueprint, request, jsonify, make_response
from .models.customer import Customer
from .models.video import Video
from datetime import datetime
import requests
import os

customer_bp = Blueprint("task", __name__, url_prefix="/customers")
video_bp = Blueprint("goal", __name__, url_prefix="/videos")

@customer_bp.route("",methods=["POST","GET"],strict_slashes=False)
def create_customer():
    """
        Input: request to create a new instance of Customer or query for all instances  
        Output: error if required attributes are missing, python dict with id key 
                and value, or list of dicts of all queries in Customer database
    """
    if request.method == "POST":
        request_body = request.get_json()
        if 'name' not in request_body:
            return make_response(jsonify({"error":"missing customer name"}), 400)
        if 'phone' not in request_body:
            return make_response(jsonify({"error":"missing phone number"}), 400)
        if 'postal_code' not in request_body:
            return make_response(jsonify({"error":"missing postal code"}), 400)
        else:
            new_customer= Customer(
                name = request_body['name'],
                postal_code = request_body['postal_code'],
                phone = request_body['phone'],
                registered_at = request_body['registered_at']
                )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(id=new_customer.id), 201
    
    if request.method == "GET":
        customers = Customer.query.all()
        customer_response = []
        for customer in customers:
            customer_response.append(customer.to_python_dict())
        return jsonify(customer_response), 200

        
@customer_bp.route("/<id>",methods=["GET","PUT","DELETE"],strict_slashes=False)
def customer(id):
    """
        Input: Request to read, edit, or delete a customer by id
        Output: 404 if the customer does not exist, dictionary of updated customer, or id of deleted
                customer id
    """
    customer = Customer.query.get(id)
    
    if not customer:
        return jsonify(message="customer id not found"), 404
    
    if request.method == "GET":
        return jsonify(customer.to_python_dict()), 200
    
    if request.method == "PUT":
        request_body = request.get_json()
        customer.name = request_body['name']
        customer.postal_code = request_body['postal_code']
        customer.phone = request_body['phone']
        customer.registered_at = request_body['registered_at']   
        db.session.commit()
        return jsonify(customer.to_python_dict()), 200

    if request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return jsonify(id=id), 200


@video_bp.route("",methods=["POST","GET"],strict_slashes=False)
def create_video():
    """
        Input: request to create a new instance of Video or query for all instances  
        Output: error if required attrbutes are missing, python dict with id key and value, or list  of dictionaries of all queries in Video database      
    """
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return make_response(jsonify({"error":"missing title of video"}), 400)
        if "release_date" not in request_body:
            return make_response(jsonify({"error":"missing video release date"}), 400)
        if "total_inventory" not in request_body:
            return make_response(jsonify({"error":"missing video total inventory"}), 400)
        new_video = Video(
            id = request_body['id'],
            title = request_body['title'],
            release_date = request_body['release_date'],
            total_inventory = request_body['total_inventory']
            )
        db.session.add(new_video)
        db.session.commit()
        return jsonify(new_video.to_python_dict()), 200
    
    if request.method == "GET":
        videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append(video.to_python_dict())
        return jsonify(videos_response), 200

@video_bp.route("/<id>",methods=["GET","PUT","DELETE"],strict_slashes=False)
def customer(id):
    """
        Input: Request to read, edit, or delete a video by id
        Output: 404 if the video does not exist, dictionary of updated video, or id of
                deleted video id
    """
    video = Video.query.get(id)
    
    if not video:
        return jsonify(errors=["video id not found"]), 404
    
    if request.method == "GET":
        return jsonify(video.to_python_dict()), 200
    
    if request.method == "PUT":
        request_body = request.get_json()
        video.title = request_body['title']
        video.release_date = request_body['release_date']
        video.total_inventory  = request_body['total_inventory']
        db.session.commit()
        return jsonify(video.to_python_dict()), 200
        
    if request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return jsonify(id=id), 200