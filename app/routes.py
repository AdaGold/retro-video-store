from flask import request,Blueprint,make_response,jsonify
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental

from datetime import datetime
import requests
import os

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

video_bp = Blueprint("video", __name__, url_prefix="/videos")

rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

@customer_bp.route("",methods=["GET"])
def get_cutomers():
    name_query=request.args.get("name")
    if name_query:
        customers=Customer.query.filter_by(name=name_query)

    else:
        customers=Customer.query.all()
    
    customers_response=[]
    for customer in customers:
        customers_response.append(customer.customer_json())
    
    return jsonify(customers_response)

@customer_bp.route("",methods=["POST"])
def post_customers():
    request_body=request.customer_json()
    if all(keys in request_body for keys in ("name","postal_code","phone")) == False:
        return {
            "details": "invalid data"
        }, 400
    else:
        new_customer = Customer(name=request_body["name"], postal_code=request_body["postal_code"], phone=request_body["phone"])
        db.session.add(new_customer)
        db.session.commit()

        customer=Customer.query.get(new_customer.id)
        return {
            "id": customer.id
        },201

@customer_bp.route("/<customer_id>",methods=["GET"])
def get_customer(customer_id):
    customer=Customer.query.get(customer_id)

    if customer is None:
        return make_response("Customer does not exist",404)
    
    return customer.customer_json(),200


@customer_bp.route("/<customer_id>",methods=["PUT"])
def put_customer(customer_id):
    customer=Customer.query.get(customer_id)

    if customer is None:
        return make_response("Customer does not exist",404)    
    
    else:
        form_data=request.get_json()
        customer.name=form_data["name"]
        customer.postal_code=form_data["postal_code"]
        customer.phone=form_data["phone"]
        db.session.commit()

        return customer.customer_json(),200


@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer=Customer.query.get(customer_id)
    if customer is None:
        return make_response("Customer does not exist",404)    
    else:
        db.session.delete(customer)
        db.session.commit()

        return {
                "id":customer.id
        },200


@video_bp.route("",methods=["GET"])
def get_videos():
    title_query=request.args.get("title")
    if title_query:
        videos=Video.query.filter_by(title=title_query)

    else:
        videos=Video.query.all()
    
    videos_response=[]
    for video in videos:
        videos_response.append(video.video_json())
    
    return jsonify(videos_response)

@video_bp.route("",methods=["POST"])
def post_videos():
    request_body=request.video_json()
    if all(keys in request_body for keys in ("title","release_date","total_inventory")) == False:
        return {
            "details": "invalid data"
        }, 400
    else:
        new_video = Video(title=request_body["title"], release_date=request_body["release_date"], total_inventory=request_body["total_inventory"])
        db.session.add(new_video)
        db.session.commit()

        video=Video.query.get(new_video.id)
        return {
            "id": video.id
        },201

@video_bp.route("/<video_id>",methods=["GET"])
def get_video(video_id):
    video=Video.query.get(video_id)

    if video is None:
        return make_response("Video does not exist",404)
    
    return video.video_json(),200

@video_bp.route("/<video_id>",methods=["PUT"])
def put_video(video_id):
    video=Video.query.get(video_id)

    if video is None:
        return make_response("Video does not exist",404)    
    
    else:
        form_data=request.get_json()
        video.title=form_data["title"]
        video.release_date=form_data["release_date"]
        video.total_inventory=form_data["total_inventory"]
        db.session.commit()

        return video.video_json(),200

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video=Video.query.get(video_id)
    if video is None:
        return make_response("Video does not exist",404)    
    else:
        db.session.delete(video)
        db.session.commit()

        return {
                "id":video.id
        },200
