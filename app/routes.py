from flask import Blueprint, request, jsonify, make_response
from werkzeug.datastructures import Authorization
from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("/<customer_id>", methods = ["GET", "PUT", "DELETE"])
def get_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    request_body = request.get_json()
    if customer is None:
        return jsonify({"details": "Customer does not exist"}), 404
    elif request.method == "GET":
        return jsonify(customer.to_json()), 200
    elif customer.name is None or customer.name is not str(customer.name):
        return jsonify({"details": "Name data is missing"}), 400
    elif customer.phone is None:
        return jsonify({"details": "Phone data is missing"}), 400
    elif customer.postal_code is None:
        return jsonify({"details": "Postal_code data is missing"}), 400
    elif request.method == "PUT":
        if all(keys in request_body for keys in ("name","postal_code","phone")) == True:
            customer.name = request_body["name"]
            customer.postal_code = request_body["postal_code"]
            customer.phone = request_body["phone"]

            db.session.add(customer)
            db.session.commit()
            return jsonify(customer.to_json()), 200
        else:
            return jsonify({"error": "Bad Request"}), 400
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return { "id" : customer.customer_id }, 200

@customers_bp.route("", methods=["GET"])
def customers_index():
    customers = Customer.query.all()
    if customers == None:
        return [], 200
    else:
        customers_response = []
        for customer in customers:
            customers_response.append(customer.to_json())
        return jsonify(customers_response), 200


@customers_bp.route("", methods = ["POST"])
def customers():
    try:
        request_body = request.get_json()
        new_customer = Customer(name =request_body["name"],
                        postal_code=request_body["postal_code"],
                        phone = request_body["phone"])

        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"id": new_customer.customer_id}), 201
    except KeyError:
        return jsonify({
            "details": "Invalid data"}), 400

# ================================== Video ========================================================

@videos_bp.route("/<video_id>", methods = ["GET", "PUT", "DELETE"])
def get_single_video(video_id):
    video = Video.query.get(video_id)
    request_body = request.get_json()
    if video is None:
        return jsonify({"details": "Video does not exist"}), 404
    elif request.method == "GET":
        return jsonify(video.to_json_video()), 200
    elif video.title is None or video.title is not str(video.title):
        return jsonify({"details": "Title data is missing"}), 400
    elif video.release_date is None:
        return jsonify({"details": "Release_date data is missing"}), 400
    elif video.total_inventory is None:
        return jsonify({"details": "Total_inventory data is missing"}), 400
    elif request.method == "PUT":
        if all(keys in request_body for keys in ("title","release_date","total_inventory")) == True:
            video.title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory = request_body["total_inventory"]

            db.session.add(video)
            db.session.commit()
            return jsonify(video.to_json_video()), 200
        else:
            return jsonify({"error": "Bad Request"}), 400
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return { "id" : video.video_id }, 200

@videos_bp.route("", methods=["GET"])
def videos_index():
    videos = Video.query.all()
    if videos == None:
        return [], 200
    else:
        videos_response = []
        for video in videos:
            videos_response.append(video.to_json_video())
        return jsonify(videos_response), 200


@videos_bp.route("", methods = ["POST"])
def videos():
    try:
        request_body = request.get_json()
        new_video = Video(title =request_body["title"],
                        release_date =request_body["release_date"],
                        total_inventory = request_body["total_inventory"])

        db.session.add(new_video)
        db.session.commit()

        return jsonify({"id": new_video.video_id}), 201
    except KeyError:
        return jsonify({
            "details": "Invalid data"}), 400