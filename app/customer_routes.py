from re import U
from app import db
from app.models.customers import Customer
from app.models.videos import Video
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime
import os, requests

customers_bp = Blueprint("cumtomers",__name__,url_prefix="/customers")
videos_bp = Blueprint("videos",__name__,url_prefix="/videos")


@customers_bp.route("", methods=["POST","GET"], strict_slashes = False)
def create_customers():

    if request.method == "POST":
        request_body = request.get_json()
        
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body: 
            return ({"details":"Invalid data"},400)
        else:
            customer = Customer(name=request_body["name"],
                        phone=request_body["phone"],
                        postal_code =request_body["postal_code"],
                        registered_at= datetime.utcnow())
            db.session.add(customer)
            db.session.commit()

            return make_response(customer.to_json(),201)
    else:
        
        customers = Customer.query.all()

        customers_response = []
        for customer in customers:
                customers_response.append(customer.to_json())

        return jsonify(customers_response)


@customers_bp.route("/<customer_id>", methods=["GET","PUT","DELETE","PATCH"], strict_slashes = False)
def a_single_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response(" ", 404)
    
    if request.method == "GET":
        return make_response(customer.to_json(),200)

    elif request.method == "PUT":
        form_data = request.get_json()
        customer.name = form_data["name"]
        customer.phone = form_data["phone"]
        customer.postal_code = form_data["postal_code"]
        db.session.commit()

        return make_response(customer.to_json(),200)

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return make_response({id:customer.customer_id})



@videos_bp.route("", methods=["POST","GET"], strict_slashes = False)
def create_videos():

    if request.method == "POST":
        request_body = request.get_json()
        
        if "title" not in request_body:
            return ({"details":"Invalid data"},400)
        else:
            video = Video(title=request_body["title"],
                        release_date=datetime.utcnow(),
                        total_inventory =request_body["total_inventory"])
            db.session.add(video)
            db.session.commit()

            return make_response(video.video_to_json(),201)
    else:
        
        videos = Video.query.all()

        videos_response = []
        for video in videos:
                videos_response.append(video.video_to_json())

        return jsonify(videos_response)


@customers_bp.route("/<video_id>", methods=["GET","PUT","DELETE","PATCH"], strict_slashes = False)
def a_single_video(customer_id):
    video = Video.query.get(customer_id)

    if video is None:
        return make_response(" ", 404)
    
    if request.method == "GET":
        return make_response(video.video_to_json(),200)

    elif request.method == "PUT":
        form_data = request.get_json()
        video.name = form_data["title"]
        video.total_inventory = form_data["total_inventory"]
        
        db.session.commit()

        return make_response(video.video_to_json(),200)

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

        return make_response({id:video.video_id})