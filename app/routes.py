from flask import Blueprint, request, make_response, jsonify
from app import db
from .models.video import Video
from .models.customer import Customer
from datetime import datetime

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customer_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def customer_functions():

    if request.method == "POST":
        request_body = request.get_json()
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response({"details": "Invalid data"}, 400)
        new_customer = Customer(name = request_body["name"], postal_code = request_body["postal_code"], phone = request_body["phone"])
        db.session.add(new_customer)
        db.session.commit()
        message = {
            "id": new_customer.customer_id
        }
        return jsonify(message), 201

    elif request.method == "GET":
        all_customers = Customer.query.all()
        message = []
        for customer in all_customers:
            message.append(customer.customer_response())
        return jsonify(message), 200

@customer_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def customer_id_functions(customer_id):
    a_customer = Customer.query.get_or_404(customer_id)

    if not a_customer:
        return jsonify({
            "Make sure you have entered the data about this person correctly. Double check that their zip code is an integer and that their phone number is a string."
        }, 404)

    if request.method == "GET":
        return jsonify(
            a_customer.customer_response()
        ), 200

    elif request.method == "PUT":
        new_customer_info = request.get_json()
        if "name" not in new_customer_info or "postal_code" not in new_customer_info or "phone" not in new_customer_info:
            return make_response({"details": "Invalid data"}, 400)

        a_customer.name = new_customer_info["name"]
        a_customer.postal_code = new_customer_info["postal_code"]
        a_customer.phone = new_customer_info["phone"]

        db.session.commit()
        return jsonify(
            a_customer.customer_response()
        ), 200

    elif request.method == "DELETE":
        db.session.delete(a_customer)
        db.session.commit()
        return jsonify({
            "id": a_customer.customer_id
        }), 200

@video_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def video_functions():

    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response({"details": "Invalid data"}, 400)

        new_video = Video(title = request_body["title"], release_date = request_body["release_date"], total_inventory = request_body["total_inventory"])
        db.session.add(new_video)
        db.session.commit()
        message = {
            "id": new_video.video_id
        }
        return jsonify(message), 201

    elif request.method == "GET":
        all_videos = Video.query.all()
        message = []
        for video in all_videos:
            message.append(video.video_response())
        return jsonify(message), 200

@video_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def video_id_functions(video_id):
    a_video = Video.query.get_or_404(video_id)

    if not a_video:
        return make_response("", 404)

    if request.method == "GET":
        return jsonify(
            a_video.video_response()
        ), 200

    elif request.method == "PUT":
        video_info = request.get_json()
        if "title" not in video_info or "release_date" not in video_info or "total_inventory" not in video_info:
            return make_response({"details": "Invalid data"}, 400)

        a_video.title = video_info["title"]
        a_video.release_date = video_info["release_date"]
        a_video.total_inventory = video_info["total_inventory"]

        db.session.commit()
        return jsonify(
            a_video.video_response()
        ), 200

    elif request.method == "DELETE":
        db.session.delete(a_video)
        db.session.commit()
        return jsonify({
            "id": a_video.video_id
        }), 200
