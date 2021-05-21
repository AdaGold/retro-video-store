from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, request, make_response, jsonify 
from app import db


customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# 
@customer_bp.route("", methods=["POST"], strict_slashes = False)
def post_customer():
    request_body = request.get_json()
    if not "name" in request_body:
        return make_response({"details": "name is missing"}), 400
    if not "postal_code" in request_body:
        return make_response({"details": "postal_code is missing"}), 400
    if not "phone" in request_body:
        return make_response({"details": "phone is missing"}), 400
    name = request_body["name"]
    postal_code = request_body["postal_code"]
    phone = request_body["phone"]
    new_customer = Customer.create(name, postal_code, phone)

    return jsonify({"id": new_customer.customer_id}), 201

#
@customer_bp.route("", methods=["GET"], strict_slashes = False)
def get_customers():
    customers = Customer.read_all()
    response_body = []
    for customer in customers:
        response_body.append(customer.to_dict())
    return jsonify(response_body), 200

# 
@customer_bp.route("/<customer_id>", methods=["GET"], strict_slashes = False)
def get_customer(customer_id):
    customer = Customer.read(customer_id)
    if not customer:
        return jsonify({"details": "customer is not found"}), 404
    return jsonify(customer.to_dict()), 200

#
@customer_bp.route("/<customer_id>", methods=["PUT"], strict_slashes = False)
def update_customer(customer_id):
    customer = Customer.read(customer_id)
    if not customer:
        return "customer does not exist", 404
    request_body = request.get_json()
    if not "name" in request_body:
        return make_response({"details": "name is missing"}), 400
    if not "postal_code" in request_body:
        return make_response({"details": "postal_code is missing"}), 400
    if not "phone" in request_body:
        return make_response({"details": "phone is missing"}), 400
    name = request_body["name"]
    postal_code = request_body["postal_code"]
    phone = request_body["phone"]
    updated_customer = Customer.update(customer_id, name, postal_code, phone)
    return jsonify(updated_customer.to_dict()), 200
    
@customer_bp.route("/<int:customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.read(customer_id)
    if not customer:
        return "customer does not exist", 404
    Customer.delete(customer_id)
    return jsonify({"id": customer_id}), 200 

@video_bp.route("", methods=["POST"], strict_slashes = False)
def post_video():
    request_body = request.get_json()
    if not "title" in request_body:
        return make_response({"details": "title is missing"}), 400
    if not "release_date" in request_body:
        return make_response({"details": "release_date is missing"}), 400
    if not "total_inventory" in request_body:
        return make_response({"details": "total_inventory is missing"}), 400
    title = request_body["title"]
    release_date = request_body["release_date"]
    total_inventory = request_body["total_inventory"]
    new_video = Video.create(title, release_date, total_inventory)

    return jsonify({"id": new_video.video_id}), 201

@video_bp.route("", methods=["GET"], strict_slashes = False)
def get_videos():
    videos = Video.read_all()
    response_body = []
    for video in videos:
        response_body.append(video.to_dict())
    return jsonify(response_body), 200
    
@video_bp.route("/<int:video_id>", methods=["GET"], strict_slashes = False)
def get_video(video_id):
    video = Video.read(video_id)
    if not video:
        return "video does not exist", 404
    return jsonify(video.to_dict()), 200

@video_bp.route("/<int:video_id>", methods=["PUT"], strict_slashes = False)
def update_video(video_id):
    video = Video.read(video_id)
    if not video:
        return "video does not exist", 404
    request_body = request.get_json()
    if not "title" in request_body:
        return make_response({"details": "title is missing"}), 400
    if not "release_date" in request_body:
        return make_response({"details": "release_date is missing"}), 400
    if not "total_inventory" in request_body:
        return make_response({"details": "total_inventory is missing"}), 400
    title = request_body["title"]
    release_date = request_body["release_date"]
    total_inventory = request_body["total_inventory"]
    video = Video.update(video_id, title, release_date, total_inventory)
    return jsonify(video.to_dict()), 200
    
@video_bp.route("/<int:video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.read(video_id)
    if not video:
        return "video does not exist", 404
    Video.delete(video_id)
    return jsonify({"id": video_id}), 200 

@rental_bp.route("/check-out", methods=["POST"], strict_slashes = False)
def rentals_checkout():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    if not type(customer_id) == int:
        return make_response({"details": "not valid customer id"}), 400
    video_id = request_body["video_id"]
    if not type(video_id) == int:
        return make_response({"details": "not valid video id"}), 400
    customer = Customer.read(customer_id)
    video = Video.read(video_id)    
    if not customer:
        return make_response({"details": "customer not found"}), 404
    if not video:
        return make_response({"details": "video not found"}), 404
    if video.available_inventory <= 0:
        return make_response({"details": "no available inventory"}), 400
    new_rental = Rental.check_out(customer, video)
    return jsonify(new_rental.to_dict()), 200

@rental_bp.route("/check-in", methods=["POST"], strict_slashes = False)
def rentals_check_in():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    customer = Customer.read(customer_id)
    video = Video.read(video_id)    
    if not customer:
        return make_response({"details": "customer not found"}), 404
    if not video:
        return make_response({"details": "video not found"}), 404
    succeed = Rental.check_in(customer, video)
    if not succeed:
        return make_response({"details": "no available rental"}), 400
    return jsonify({
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }), 200

@customer_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes = False)
def get_videos_checked_out(customer_id):
    response_body = []
    customer = Customer.read(customer_id)
    if not customer:
        return jsonify({"details": "customer is not found"}), 404
    rentals = Rental.read_checked_out_by_customer(customer_id)
    format_string = "%Y-%m-%d"
    for customer, video, rental in rentals:
        response_body.append({
            "release_date": video.release_date.strftime(format_string),
            "title": video.title,
            "due_date": rental.due_date.strftime(format_string)
        })
    return jsonify(response_body), 200 

@video_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes = False)
def get_customers_checked_out(video_id):
    response_body = []
    video = Video.read(video_id)
    if not video:
        return jsonify({"details": "video is not found"}), 404
    rentals = Rental.read_checked_out_by_video(video_id)
    format_string = "%Y-%m-%d"
    for customer, video, rental in rentals:
        response_body.append({
            "due_date": rental.due_date.strftime(format_string),
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        })
    return jsonify(response_body), 200
   
   


