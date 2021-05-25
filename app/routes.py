from flask import Blueprint, request, jsonify, make_response
from werkzeug.datastructures import Authorization
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from datetime import datetime, timedelta

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

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
        # explain this
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

# =========================== Rental Routes ========================

# @rentals_bp.route("/<video_id>", methods = ["GET", "PUT", "DELETE"])
# def get_single_video(video_id):
#     video = Video.query.get(video_id)
#     request_body = request.get_json()
#     if video is None:
#         return jsonify({"details": "Video does not exist"}), 404
#     elif request.method == "GET":
#         return jsonify(video.to_json_video()), 200
#     elif video.title is None or video.title is not str(video.title):
#         return jsonify({"details": "Title data is missing"}), 400
#     elif video.release_date is None:
#         return jsonify({"details": "Release_date data is missing"}), 400
#     elif video.total_inventory is None:
#         return jsonify({"details": "Total_inventory data is missing"}), 400
#     elif request.method == "PUT":
#         if all(keys in request_body for keys in ("title","release_date","total_inventory")) == True:
#             video.title = request_body["title"]
#             video.release_date = request_body["release_date"]
#             video.total_inventory = request_body["total_inventory"]

#             db.session.add(video)
#             db.session.commit()
#             return jsonify(video.to_json_video()), 200
#         else:
#             return jsonify({"error": "Bad Request"}), 400
#     elif request.method == "DELETE":
#         db.session.delete(video)
#         db.session.commit()
#         return { "id" : video.video_id }, 200

# @videos_bp.route("", methods=["GET"])
# def videos_index():
#     videos = Video.query.all()
#     if videos == None:
#         return [], 200
#     else:
#         videos_response = []
#         for video in videos:
#             videos_response.append(video.to_json_video())
#         return jsonify(videos_response), 200


@rentals_bp.route("/check-out", methods = ["POST"])
def rentals_check_out():

    if request.method == "POST":
        request_body = request.get_json()
        request_body_customer = request_body.get('customer_id')
        request_body_video = request_body.get('video_id')
        if request_body_customer == None:
            return jsonify({"details":"customer does not exist"}), 404
        elif request_body_video == None:
            return jsonify({"details": "video does not exist"}), 404
        elif request_body_video.get('available_inventory') == 0:
            return jsonify({"details": "There is not available inventory"}), 400
        else:
            checked_out = Rental(
                video_check_out_count = request_body_customer["video_check_out_count"] + 1, 
                available_inventory = request_body_video["available_inventory"] -1,
                due_date = datetime.now() + timedelta(days=7))

            db.session.add(checked_out)
            db.session.commit()

            return jsonify({"customer_id": request_body_customer, 
                            "video_id": request_body_video,
                            "due_date": datetime.today() + timedelta(days=7),
                            "videos_checked_out_count": checked_out.videos_checked_out_count,
                            "available_inventory": checked_out.update_inventory
                            }), 200

@rentals_bp.route("/check-in", methods = ["POST"])
def rentals_check_in():
    if request.method == "POST":
        request_body = request.get_json()
        request_body_customer = request_body.get('customer_id')
        request_body_video = request_body.get('video_id')
        if request_body_customer == None:
            return jsonify({"details":"customer does not exist"}), 404
        elif request_body_video == None:
            return jsonify({"details": "video does not exist"}), 404
        elif request_body.customer_id or request_body.video_id not in request_body:
            return jsonify({"details": "There is not available inventory"}), 400
        else:
            checked_out = Rental(
                video_check_out_count = request_body_customer["video_check_out_count"] - 1, 
                available_inventory = request_body_video["available_inventory"] +1,
                due_date = datetime.now() + timedelta(days=7))

            db.session.add(checked_out)
            db.session.commit()

            return jsonify({"customer_id": request_body_customer, 
                            "video_id": request_body_video,
                            "due_date": datetime.today() + timedelta(days=7),
                            "videos_checked_out_count": checked_out.videos_checked_out_count,
                            "available_inventory": checked_out.update_inventory
                            }), 200
@customers_bp.route("/<customer_id>/rentals", methods = ["GET"])
def checked_out_videos():
    customers = Customer.query.all()
    if request.customer_id is None:
        return jsonify({"details": "cutomer does not exist"}), 404
    elif customers == None:
        return [], 200
    else:
        customers_response = []
        for customer in customers:
            customers_response.append(customer.to_json())
        return jsonify(customers_response), 200

@videos_bp.route("/<video_id>/rentals", methods = ["GET"])
def checked_out_videos():
    videos = Video.query.all()
    if request.video_id is None:
        return jsonify({"details": "video does not exist"}), 404
    elif videos == None:
        return [], 200
    else:
        videos_response = []
        for video in videos:
            videos_response.append(video.to_json_video())
        return jsonify(videos_response), 200