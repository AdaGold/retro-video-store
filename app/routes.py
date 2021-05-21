from flask import Blueprint
from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, make_response, jsonify
import datetime
import os 
import requests 

#==== Customers ====#
customers_bp = Blueprint("customers",__name__,url_prefix="/customers")

@customers_bp.route("", methods=["GET","POST"])
def handle_customers():
    if request.method == "GET":
        customers = Customer.query.all()
        customers_list = []  
        for customer in customers:
            customers_list.append(customer.customer_to_json())
        return jsonify(customers_list), 200
    
    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_customer = Customer(
                name=request_body["name"],
                postal_code=request_body["postal_code"],
                phone=request_body["phone"])
        except KeyError:
            return make_response({"details" : "Invalid data"}, 400)
    
        db.session.add(new_customer)
        db.session.commit()
        return make_response(new_customer.customer_to_json(), 201)


@customers_bp.route("/<customer_id>", methods=["GET"])
def handle_one_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    if request.method == "GET":
        return jsonify(customer.customer_to_json()), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        try:
            customer.name = request_body["name"]
            customer.postal_code = request_body["postal_code"]
            customer.phone = request_body["phone"]
        except KeyError:
            return make_response({"details" : "Invalid data"}, 400)

        db.session.commit()
        return make_response(customer.to_dict(), 200)

    elif request.method == "DELETE":
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return ({"id" : int(customer_id)}, 200)


# ==== Videos ==== 
videos_bp = Blueprint("videos",__name__,url_prefix="/videos")
@customers_bp.route("", methods=["GET","POST"])
def handle_customers():
    if request.method == "GET":
        videos = Video.query.all()
        videos_list = []  
        for video in videos:
            videos_list.append(video.video_to_json())
        return jsonify(videos_list), 200
    
    elif request.method == "POST":
        request_body = request.get_json()
        try:
            new_video = Video(
                title=request_body["title"],
                release_date=request_body["release_date"],
                total_inventory=request_body["total_inventory"])
        except KeyError:
            return make_response({"details" : "Invalid data"}, 400)
    
        db.session.add(new_video)
        db.session.commit()
        return make_response(new_video.video_to_json(), 201)


@customers_bp.route("/<video_id>", methods=["GET"])
def handle_one_video(video_id):
    video = Video.query.get_or_404(video_id)

    if request.method == "GET":
        return jsonify(video.video_to_json()), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        try:
            video.title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory = request_body["total_inventory"]
        except KeyError:
            return make_response({"details" : "Invalid data"}, 400)

        db.session.commit()
        return make_response(video.to_dict(), 200)

    elif request.method == "DELETE":
        video = Video.query.get_or_404(video_id)
        db.session.delete(video)
        db.session.commit()
        return ({"id" : int(video_id)}, 200)
