from flask import Blueprint, request, jsonify, make_response
from werkzeug.datastructures import Authorization
from app import db
from app.models.customer import Customer
from app.models.video import Video


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET"])
def customers_index():
    customers = Customer.query.all()
    if customers == None:
        return [], 200
    else:
        customers_response = []
        for customer in customers:
            customers_response.append(customer.to_json())
        return jsonify([customers_response]), 200

@customers_bp.route("/<customer_id>", methods = ["GET", "PUT"])
def get_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return jsonify(None), 404
    elif request.name == None or request.postal_code == None or request.phone == None:
        return jsonify("Your request was incomplete"), 400
    elif request.method == "GET":
        return customer.to_json(), 200
    elif request.method == "PUT":
        request_body = request.get_json()
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
        db.session.add(customer)
        db.session.commit()
        return jsonify(customer.to_json()), 200
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return { "id" : customer.customer_id }, 200

@customers_bp.route("", methods = ["POST"])
def customers():
    try:
        # This portion is the POST request
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

@videos_bp.route("", methods=["GET"])
def videos_index():
    videos = Video.query.all()
    if videos == None:
        return [], 200
    else:
        videos_response = []
        for video in videos:
            videos_response.append(video.to_json_video())
        return jsonify([{videos_response}]), 200

@videos_bp.route("/<video_id>", methods = ["GET", "PUT"])
def get_single_video(video_id):
    video = Video.query.get(video_id)
    if video == None:
        return jsonify(None), 404
    elif request.title == None or request.release_date == None or request.total_inventory == None:
        return jsonify("Your request was incomplete"), 400
    elif request.method == "GET":
        return video.to_json_video(), 200
    elif request.method == "PUT":
        request_body = request.get_json()
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
        db.session.commit()
        return jsonify(video.to_json_video()), 200
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return { "id" : video.video_id }, 200

@videos_bp.route("", methods = ["POST"])
def videos():
    try:
        # This portion is the POST request
        request_body = request.get_json()
        new_video = Video(name = request_body["title"],
                        postal_code= request_body["release_date"],
                        phone = request_body["total_inventory"])

        db.session.add(new_video)
        db.session.commit()

        return jsonify({"id": new_video.video_id}), 201
    except KeyError:
        return jsonify({
            "details": "Invalid data"}), 400