from datetime import datetime
from flask import Blueprint, json, make_response, request, jsonify
from app import db
from app.models.customer import Customer
from app.models.video import Video
import os
import requests

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

                                       ### Crud Customers ###
#decided to combine the post and get.

@customers_bp.route("", methods=["GET", "POST"], strict_slashes = False)
def customer_main_func():

    if request.method == "POST":
        customer_info = request.get_json()
        
        if "name" not in customer_info or "postal_code" not in customer_info or "phone" not in customer_info:
            return make_response({"details":"invalid data"}, 400)
        
        new_customer = Customer(
        name = customer_info["name"],
        postal_code = customer_info["postal_code"],
        phone = customer_info["phone"]
        )
        db.session.add(new_customer)
        db.session.commit() 
        
        response = {
            "id": new_customer.customer_id
        }
        return jsonify(response), 201

    elif request.method == "GET":
        customers = Customer.query.all()
        response = []
        for customer in customers:
            response.append(customer.resp_json())
        return jsonify(response), 200

#change code to combine get, put, delete methods, easier to follow in my brain. Def went back to the style I had on task_list_api. 


@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes = False)
def customer_id_main_func(customer_id):
    customer = Customer.query.get_or_404(customer_id)


    if not customer:
        return jsonify({
            "Customer info invalid. Try again!"
        }, 404)

    if request.method == "GET":
        return jsonify(
            customer.resp_json()
        ), 200
    
    elif request.method == "PUT":
        request_body = request.get_json()
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response({
                "details": "invalid data"
            }, 400)

        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
        db.session.commit()

        return jsonify(
            customer.resp_json()
        ), 200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        
        return jsonify({
            "id": customer.customer_id
        }), 200


                                              ### CRUD VIDEO ###

@videos_bp.route("", methods=["GET", "POST"], strict_slashes = False)
def video_main_func():

    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response({
                "details": "invalid data"
            }, 400)

        single_video = Video(
        title= request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"]
        )
        db.session.add(single_video)
        db.session.commit()
        response = {
            "id": single_video.video_id
        }
        return jsonify(response), 201

    elif request.method == "GET":
        all_videos =Video.query.all()
        response = []

        for video in all_videos:
            response.append(video.resp_json())
        return jsonify(response), 200


@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"], strict_slashes = False)
def video_func(video_id):
    video = Video.query.get_or_404(video_id)
    
    if not video:
        return make_response("", 404)

    if request.method == "GET":
        return jsonify(
            video.resp_json()
        ), 200

    elif request.method == "PUT":
        about_video = request.get_json()
        if "title" not in about_video or "release_data" not in about_video or "total_inventory" not in about_video:
            return make_response({"details": "invalid data"}, 400)

        video.title = about_video["title"]
        video.release_date = about_video["release_date"]
        video.total_inventory = about_video["total_inventory"]
        
        db.session.commit()
        return jsonify(
            video.resp_json()
        ), 200
       
    elif request.method == "DELETE":

        db.session.delete(video)
        db.session.commit()

        return jsonify({
            "id": video.video_id
        }), 200