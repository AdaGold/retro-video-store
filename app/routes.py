# from flask import Blueprint
from app import db
from app.models.customer import Customer
from flask import request, Blueprint, make_response
from flask import jsonify
import time
import datetime
from datetime import datetime 
import requests
from flask import current_app as app
import os 
from app.models.video import Video



customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers():
    
    if request.method == "GET":  
        customers = Customer.query.all()
        customers_response = []

        for customer in customers:
        
            customers_response.append(customer.to_json())
            
            

        return jsonify(customers_response)
    

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customers():
    
    
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
        
    
    customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"])

    if customer.registered_at == None:
        customer.registered_at = datetime.now()

    db.session.add(customer)
    db.session.commit()

    return(
        {
            "id":customer.customer_id 
    }, 201)


    

@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_custumer(customer_id):
    # Try to find the task with the given id

    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response({"details": "Invalid data"}, 404)

    if request.method == "GET":
        
        return make_response(customer.to_json(),200)

    elif request.method == "PUT":
        
        request_body = request.get_json()
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)
            
        form_data = request.get_json()
        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]

        db.session.commit()

        return jsonify({"customer": customer.to_json()})

    

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
    return make_response({
        "id": customer.customer_id
    }, 200)
        
        # return make_response(f"Customer {customer.task_id} \"{customer.name}\" successfully deleted")



# ******************************************************************************************


@videos_bp.route("", methods=["GET"], strict_slashes=False)
def videos():
    # if request.method == "GET":  
    videos = Video.query.all()

    if videos is None:
        return make_response("", 404)

    videos_response = []

    for video in videos:
        videos_response.append(video.to_json())

    print(videos_response)       
    return jsonify(videos_response)
    

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_videos():
    
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)
        
            
    video = Video(title=request_body["title"],
                            release_date=request_body["release_date"],
                            total_inventory=request_body["total_inventory"])


    db.session.add(video)
    db.session.commit()

    return (
        {
            "id":video.video_id 
    }, 201)

@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response("", 404)

    if request.method == "GET":
        
        return jsonify({"video": video.to_json()}),200

    elif request.method == "PUT":
        
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)
            
        form_data = request.get_json()
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

        db.session.commit()

        return jsonify({"video": video.to_json()})

    

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
    return make_response({
        "id": video.video_id
    }, 200)