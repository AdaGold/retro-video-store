from flask import Blueprint
import flask_migrate
from app import db 
from app.models.video import Video 
from app.models.customer import Customer
from flask import request, Blueprint, make_response 
from flask import jsonify
from datetime import date
import requests
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

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
            customers_response.append(customer.to_json)
        return jsonify(customers_response), 200 

    elif request.method == "POST":
        request_body = request.get_json()
        if "name" in request_body and "postal code" in request_body and "phone" in request_body:
            new_customer = Customer(name = request_body["name"],
                            postal_code = request_body["postal code"],
                            phone = request_body["phone"])
            db.session.add(new_customer)
            db.session.commit()
            return jsonify(new_customer), 201

        else:
            return {
                "details": "Invalid data"
            }, 400

@customers_bp.route("/<id>", methods = ["PUT", "GET", "DELETE"], strict_slashes=False)
def customer_by_id(id):
    customer = Customer.query.get(id)
    if request.method == "GET":
        if customer:
            if customer.id:
                return {"customer": customer.to_json()}
            else:
                return {
                    "customer": {
                    "id": customer.id,
                    "name": customer.name,
                    "postal code": customer.postal_code,
                    "phone": customer.phone,
                    "registered_at": customer.registered_at,
                    "videos checked out count": customer.videos_checked_out_count}
            }, 200

        else:
            return (f"None", 404)

    elif request.method == "PUT":
        if customer:
            request_body = request.get_json()
            customer.name = request_body["name"]
            customer.postal_code = request_body["postal code"]
            customer.phone = request_body["phone"]
            customer.registered_at = request_body["registered at"]
            db.session.commit()
            return {
                    "customer": {
                    "id": customer.id,
                    "name": customer.name,
                    "postal code": customer.postal_code,
                    "phone": customer.phone,
                    "registered_at": customer.registered_at,
                    "videos checked out count": customer.videos_checked_out_count}
            }, 200

        else:
            return (f"None", 404)

    elif request.method == "DELETE":
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return {
                "details": f"Customer {customer.id} \"{customer.name}\" successfully deleted"
            }, 200
        else:
            return (f"None", 404)

    else:
        return (f"None", 404)

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

    elif request.method == "POST":
        request_body = request.get_json()
        if "title" in request_body:
            new_video = Video(title = request_body["title"])
            db.session.add(new_video)
            db.session.commit() 

            return jsonify(new_video), 201
        else:
            return {
                "details": "Invalid data"
            }, 400


@videos_bp.route("/<id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def video_by_id(id):
    video = Video.query.get(id)
    if request.method == "GET":
        if video:
            return video.to_json, 200

        else:
            return (f"None", 404)

    elif request.method == "PUT":
        if video:
            request_body = request.get_json()
            video.title = request_body["title"]
            db.session.commit()

            return video.to_json, 200

        else:
            return (f"None", 404)

    elif request.method == "DELETE":
        if video:
            db.session.delete(video)
            db.session.commit()
            return {
                "details": f"Video {video.id} \"{video.title}\" successfully deleted"
            }, 200
        else:
            return (f"None", 404)

    else:
        return (f"None", 404)
