from flask import Blueprint, request, make_response, jsonify
from app import db
from .models.video import Video
from .models.customer import Customer
from datetime import datetime

customer_bp = Blueprint("customer", __name__, url_prefix="/customer")
video_bp = Blueprint("video", __name__, url_prefix="/video")

@customer_bp.route("", methods=["GET", "POST"])
def customer_functions():

    if request.method == "POST":
        request_body = request.get_json()
        new_customer = Customer(name = request_body["customer_name"], postal_code = request_body["postal_code"], phone = request_body["phone_number"])
        db.session.add(new_customer)
        db.session.commit()
        message = {
            "id": new_customer["customer_id"]
        }
        return jsonify(message), 201

    elif request.method == "GET":
        all_customers = Customer.query.all()
        message = []
        for customer in all_customers:
            message.append(customer.customer_response())
        return jsonify(message), 200

@customer_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"])
def customer_id_functions(customer_id):
    a_customer = Customer.query.get(customer_id)

    if not a_customer:
        return make_response({
            "Make sure you have entered the data about this person correctly. Double check that their zip code is an integer and that their phone number is a string."
        }, 200)

    if request.method == "GET":
        return {
            a_customer.customer_response()
        }, 200

    elif request.method == "PUT":
        customer_info = request.get_json()

        a_customer.name = customer_info["name"]
        a_customer.postal_code = customer_info["postal_code"]
        a_customer.phone_number = customer_info["phone"]

        db.session.commit()
        return {
            a_customer.customer_response()
        }, 200

    elif request.method == "DELETE":
        db.session.delete(a_customer)
        db.session.commit()
        return {
            "id": f"The customer with the id {a_customer.customer_id} has been deleted."
        }, 200

@video_bp.route("", methods=["GET", "POST"])
def video_functions():

    if request.method == "POST":
        request_body = request.get_json()
        new_video = Video(title = request_body["video_title"], release_date = request_body["release_date"], total_inventory = request_body["inventory"])
        db.session.add(new_video)
        db.session.commit()
        message = {
            "id": new_video["video_id"]
        }
        return jsonify(message), 201

    elif request.method == "GET":
        all_videos = Video.query.all()
        message = []
        for video in all_videos:
            message.append(video.video_response())
        return jsonify(message), 200

@video_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def video_id_functions(video_id):
    a_video = Video.query.get(video_id)

    if not a_video:
        return make_response({
            "Make sure you have entered the data about this person correctly. Double check that their zip code is an integer and that their phone number is a string."
        }, 200)

    if request.method == "GET":
        return {
            a_video.video_response()
        }, 200

    elif request.method == "PUT":
        video_info = request.get_json()

        a_video.title = video_info["title"]
        a_video.release_date = video_info["release_date"]
        a_video.inventory = video_info["total_inventory"]

        db.session.commit()
        return {
            a_video.video_response()
        }, 200

    elif request.method == "DELETE":
        db.session.delete(a_video)
        db.session.commit()
        return {
            "id": f"The customer with the id {a_video.video_id} has been deleted."
        }, 200
