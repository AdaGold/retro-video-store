from app.models.customer import Customer
from app.models.video import Video

from app import db
from flask import json, request, Blueprint, make_response, jsonify
import os
import requests

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

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

def valid_customer_data(request_body):
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return False
    # How can you validate data types for not required params?
    # elif not isinstance(request_body["name"],str) or not isinstance(request_body["phone"],str) or not isinstance(request_body["postal_code"],str):
    #     return False
    return True

'''
CRUD routes for Videos

POST /videos
PUT /videos/<id>
DELETE /videos/<id>
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


def valid_video_data(request_body):
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return False
    return True