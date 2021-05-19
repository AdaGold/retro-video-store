from app.models.customer import Customer
from app.models.video import Video

from app import db
from flask import json, request, Blueprint, make_response, jsonify
import os
import requests

# Create blueprints
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

'''
CRUD routes for Customers
'''
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_list = []
    for customer in customers:
        customers_list.append(customer.get_response())

    return jsonify(customers_list), 200

@customers_bp.route("/<id>", methods=["GET"])
def get_customer_id(id):
    customer = Customer.query.get(id)

    if customer == None: 
        return {"error":f"Customer ID {id} not found."}, 404
    return jsonify(customer.get_response()),200

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()

    if not valid_customer_data(request_body):
            return {"details":"Invalid data"}, 400

    new_customer = Customer(
                        name=request_body["name"],
                        postal_code=request_body["postal_code"],
                        phone=request_body["phone"])
    db.session.add(new_customer)
    db.session.commit()
    return {"id":new_customer.id},201

@customers_bp.route("/<id>", methods=["PUT"])
def update_customer_info(id):
    customer = Customer.query.get(id)

    if customer == None: 
        return {"error":f"Customer ID {id} not found."}, 404

    request_body = request.get_json()
    if not valid_customer_data(request_body):
            return {"details":"Invalid data"}, 400

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]
    db.session.commit()
    return jsonify(customer.get_response()), 200
    
@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer == None: 
        return {"error":f"Customer ID {id} not found."}, 404
    db.session.delete(customer)
    db.session.commit()
    return {
        "id":customer.id
    }, 200

# Helper Function to ensure request body contians valid data
def valid_customer_data(request_body):
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return False
    # elif not isinstance((request_body["name"]),str) or not isinstance((request_body["phone"]),str) or not isinstance((request_body["postal_code"]),str):
    elif (type(request_body["name"])) is not str or (type(request_body["phone"])) is not str or (type(request_body["postal_code"])) is not str:
        return False
    if "videos_checked_out_count" in request_body and (type(request_body["videos_checked_out_count"])) is not int:
        return False
    return True

'''
CRUD routes for Videos
'''
@videos_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    videos_list = []
    for video in videos:
        videos_list.append(video.get_response())

    return jsonify(videos_list), 200

@videos_bp.route("/<id>", methods=["GET"])
def get_video_by_id(id):
    video = Video.query.get(id)

    if video == None: 
        return {"error":f"Video ID {id} not found."}, 404
    return jsonify(video.get_response()),200

@videos_bp.route("", methods=["POST"])
def create_new_video():
    request_body = request.get_json()
    if not valid_video_data(request_body):
            return {"details":"Invalid data"}, 400
    new_video = Video(
                        title=request_body["title"],
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"])
    db.session.add(new_video)
    db.session.commit()
    return {"id":new_video.id},201

@videos_bp.route("/<id>", methods=["PUT"])
def update_video_info(id):
    video = Video.query.get(id)

    if video == None: 
        return {"error":f"Video ID {id} not found."}, 404

    request_body = request.get_json()
    if not valid_video_data(request_body):
            return {"details":"Invalid data"}, 400

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]
    db.session.commit()
    return jsonify(video.get_response()), 200

@videos_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    video = Video.query.get(id)
    if video == None: 
        return {"error":f"Video ID {id} not found."}, 404
    db.session.delete(video)
    db.session.commit()
    return {
        "id":video.id
    }, 200

def valid_video_data(request_body):
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return False
    return True

'''
POST /rentals/check-out
POST /rentals/check-in
GET /customers/<id>/rentals
GET /videos/<id>/rentals
'''

@rentals_bp.route("/check-out", methods=["POST"])
def check_out_rental():
    request_body = request.get_json()

    user_id = request_body["customer_id"]
    rental_id = request_body["video_id"]

    if user_id == None:
        return {"error":"Please provide a customer ID"}
    if rental_id == None:
        return {"error":"Please provide a video ID"}

    customer = Customer.query.get(user_id)
    video = Video.query.get(rental_id)

    if customer == None:
        return {"error":"Please provide a customer ID"}
    if rental_id == None:
        return {"error":"Please provide a video ID"}
        
    '''
    increase the customer's videos_checked_out_count by one
    decrease the video's available_inventory by one
    create a due date. The rental's due date is the seven days from the current date.
    '''

@rentals_bp.route("", methods=["POST"])
def check_in_rental():
    pass

@customers_bp.route("/<id>", methods=["GET"])
def get_customer_check_outs():
    pass

@videos_bp.route("/<id>", methods=["GET"])
def get_customers_who_checked_out_video():
    pass