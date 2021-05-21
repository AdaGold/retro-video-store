from flask import Blueprint
import flask_migrate
from app import db
from app.models.video import Video 
from app.models.customer import Customer
from app.models.rental import Rental
from flask import request, Blueprint, make_response, Response 
from flask import jsonify
from datetime import datetime
import requests
import os
import json

# Creating my blueprints here 
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# Wave 1 ==================================================================>

# GET all of the customers. Ability to sort asc or desc by customer name 
@customers_bp.route("", methods = ["POST", "GET"], strict_slashes=False)
def handle_customer():
    if request.method == "GET":
        query_param_value = request.args.get("sort")
        if query_param_value == "asc":
            customers = Customer.query.order_by(Customer.name.asc())
        
        elif query_param_value == "desc":
            customers = Customer.query.order_by(Customer.name.desc())
        
        else:
            customers = Customer.query.all()

        customers_response = []
        for customer in customers:
            customers_response.append(customer.to_json())
        return jsonify(customers_response), 200 

# POST a new customer with or without all required fields filled in 
    elif request.method == "POST":
        request_body = request.get_json()
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        new_customer = Customer(
                        name = request_body["name"],
                        postal_code = request_body["postal_code"],
                        phone = request_body["phone"],
                        registered_at = datetime.now())
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.to_json()), 201

# GET customer by their id
@customers_bp.route("/<id>", methods = ["PUT", "GET", "DELETE"], strict_slashes=False)
def customer_by_id(id):
    customer = Customer.query.get(id)
    
    if request.method == "GET":
        if customer:
            if not customer.is_int():
                return {
                    "message": "invalid data",
                    "success": False 
                }, 400
            
            if customer.id:
                return make_response(customer.to_json(), 200)

        else:
            return jsonify(details="Not Found"), 404


# PUT an update on an exsisting customer 
    elif request.method == "PUT":
        request_body = request.get_json()
        print(request_body)
        if request_body != None:
            if ("name" not in request_body or 
                "postal_code" not in request_body or 
                "phone" not in request_body):
                return jsonify(details="Bad request"), 400
            if customer:
                customer.name = request_body["name"]
                customer.postal_code = request_body["postal_code"]
                customer.phone = request_body["phone"]
                db.session.commit()
                return customer.to_json(), 200
            else:
                return jsonify(""), 404

        else:
            return jsonify(""), 404


# DELETE an existing customer by id
    elif request.method == "DELETE":
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return jsonify(id=int(id)), 200

        else:
            return jsonify(""), 404

# GET all videos and ability to sort by asc or desc 
@videos_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def handle_video():
    if request.method == "GET":  
        query_param_value = request.args.get("sort")
        if query_param_value == "asc":
            video = Video.query.order_by(Video.title.asc())

        elif query_param_value == "desc":
            videos = Video.query.order_by(Video.title.desc())

        else:
            videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append(video.to_json())
        return jsonify(videos_response), 200

# POST new video 
    elif request.method == "POST":
        request_body = request.get_json()
    if ("title" not in request_body or 
        "release_date" not in request_body or 
        "total_inventory" not in request_body):
        return jsonify(details="Bad request"),400
    
    new_video = Video(title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"])
    
    db.session.add(new_video)
    db.session.commit()
    
    return make_response(jsonify(id=new_video.id) ,201)

# GET video by id 
@videos_bp.route("/<id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def video_by_id(id):
    video = Video.query.get(id)
    if request.method == "GET":
        if video:
            if not video.is_int():
                return {
                "message": "id must be an integer",
                "success": False
            }, 400
        
            return make_response(video.to_json(), 200)
        else: #if there is no video 
            return Response ("", 404)

# PUT an update on a current video by id
    elif request.method == "PUT":
        video = Video.query.get(id)
        
        if video == None or not video:
            return Response("", status=404)
        
        form_data = request.get_json()
        
        if not form_data or not form_data["title"] or not form_data["release_date"] or not form_data["total_inventory"]:
            return Response("", 400)

        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]
        
        db.session.commit()
        
        return video.to_json(), 200

# DELETE video by id 
    elif request.method == "DELETE":
        video = Video.query.get(id)
        if video == None:
            return Response("", status=404)
    
        if video:
            db.session.delete(video)
            db.session.commit()
            
            return jsonify(id=int(id)), 200


# Wave 2 ==================================================================>

# GET new rentals from customer 
@rentals_bp.route("/check-out",methods=["POST"], strict_slashes=False)
def checkout_rental():
    request_body = request.get_json()
    video = Video.query.get(request_body["video_id"])
    customer = Customer.query.get(request_body["customer_id"])

    if "customer_id" not in request_body.keys() or "video_id" not in request_body.keys():
        return jsonify(details="Not Found"), 404

    if not customer.is_int(request_body["customer_id"]):
        return jsonify(details="Bad Request"), 400

    if not video.is_int(request_body["video_id"]):
        return jsonify(details="Bad Request"), 400

    if video is None:
        return jsonify(details="Not Found"), 404
    
    if customer is None:
        return jsonify(details="Not Found"), 404
    
    if video.get_available_inventory() == 0:
        return jsonify(details="No available inventory"), 400

    new_rental = Rental(customer_id = request_body["customer_id"],
                        video_id = request_body["video_id"])
    
    db.session.add(new_rental)
    db.session.commit()

    return {
        "customer_id": customer.id,
        "video_id": video.id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.current_videos(),
        "available_inventory": video.get_available_inventory()
    }, 200

    # return a rental from customer
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def return_rental():
    request_body = request.get_json()
    rental = Rental.query.filter(Rental.customer_id == request_body["customer_id"], Rental.video_id == request_body["video_id"]).first()
    customer = Customer.query.get(request_body["customer_id"])
    customer_videos = customer.video

    if "customer_id" not in request_body.keys() or "video_id" not in request_body.keys():
        return jsonify(details="Not Found"), 404
    
    if rental is None:
        return jsonify(details="Bad Request"), 400

    for video in customer_videos:
        if video.id == request_body["video_id"]:
            customer_videos.remove(video)

    db.session.commit()
    
    video = Video.query.get(request_body["video_id"])

    return {
            "customer_id": customer.id,
            "video_id": video.id,
            "videos_checked_out_count": customer.current_videos(),
            "available_inventory": video.get_available_inventory()
        }, 200


# GET list if video customers 
# @videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
# def get_video_customers(video_id):
#     def is_int(self):
#         try:
#             return int(self.id)
#         except ValueError:
#             return False

#     if not is_int(video_id):
#         return ("", 400)

#     rentals = Rental.query.filter(Rental.video_id == video_id)

#     if rentals is None:
#         return ("", 404)
    
#     list_of_rentals = []

#     for rental in rentals:
#         customer = Customer.query.get(rental.id)
#         list_of_rentals.append(
#         {"due_date": rental.due_date,
#         "name": customer.name,
#         "phone": customer.phone,
#         "postal_code": customer.postal_code}
#         )
    
#     return jsonify(list_of_rentals), 200