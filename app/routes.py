from flask import Blueprint, request, make_response, jsonify
from app import db
from .models.video import Video
from .models.customer import Customer
from .models.rental import Rental
from datetime import datetime

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

#Customer Functions/Wave 1*******************************************************************************************************************************************
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

#Video Functions/Wave 1********************************************************************************************************************************************
@video_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def video_functions():

    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response({"details": "Invalid data"}, 400)

        new_video = Video(title = request_body["title"], release_date = request_body["release_date"], total_inventory = request_body["total_inventory"],
            available_inventory = request_body["total_inventory"])
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

#Rental Funtions/Wave2*******************************************************************************************************************************************
@rental_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out_video():
    request_body = request.get_json()

    a_video_id = request_body["video_id"]
    a_customer_id = request_body["customer_id"]
    
    if a_video_id == None or not isinstance(a_video_id, int):
        return make_response({"details":"Give video id"}, 400)

    if a_customer_id == None or not isinstance(a_customer_id, int):
        return make_response({"details":"Give video id"}, 400)

    a_video = Video.query.get_or_404(a_video_id)
    a_customer = Customer.query.get_or_404(a_customer_id)

    if a_video.available_inventory < 1:
        return make_response({"details":"There are no videos like this available"}, 400)

    a_video.available_inventory -= 1
    a_customer.videos_checked_out_count += 1

    checked_out_video = Rental(customer_id = a_customer_id, video_id = a_video_id)

    db.session.add(checked_out_video)
    db.session.commit()

    return jsonify(
        checked_out_video.rental_response()
    ), 200

@rental_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in_video():
    request_body = request.get_json()

    a_video_id = request_body["video_id"]
    a_customer_id = request_body["customer_id"]
    
    if a_video_id == None or not isinstance(a_video_id, int):
        return make_response({"details":"Give video id"}, 400)

    if a_customer_id == None or not isinstance(a_customer_id, int):
        return make_response({"details":"Give video id"}, 400)

    a_video = Video.query.get_or_404(a_video_id)
    a_customer = Customer.query.get_or_404(a_customer_id)
        
    rental = Rental.query.filter_by(customer_id = a_customer_id, video_id = a_video_id).one_or_none()
    if not rental:
        return make_response({"details": "This rental doesn't exist"}, 400)
    checked_in_video = rental

    a_video.available_inventory += 1
    a_customer.videos_checked_out_count -= 1

    db.session.delete(rental)
    db.session.commit()

    response = {
        "customer_id": checked_in_video.customer_id,
        "video_id": checked_in_video.video_id,
        "videos_checked_out_count": a_customer.videos_checked_out_count,
        "available_inventory": a_video.available_inventory
    }

    return jsonify(
        response
    ), 200

@customer_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def customer_rentals(customer_id):
    if not Customer.query.get(customer_id):
        return make_response({"details": "Customer does not exist"}, 404)

    #use the join query for customer. pattern customer, video, customer
    all_rentals = db.session.query(Rental).join(Customer, Customer.customer_id==Rental.customer_id)\
        .join(Video, Video.video_id==Rental.video_id).filter(Customer.customer_id == customer_id).all()

    list_of_rentals = []
    for rental in all_rentals:
        #create the return statement and to get the values the set up is the same how rental response is set up. but instead of self use all_rentals. because of the join clause
        list_of_rentals.append({
            "release_date": Video.query.get(rental.video_id).release_date,
            "title": Video.query.get(rental.video_id).title,
            "due_date": rental.due_date
        })
    return jsonify(list_of_rentals), 200

@video_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def video_rentals(video_id):
    if not Video.query.get(video_id):
        return make_response({"deatils": "Video does not exist"}, 404)

    #do the same as above just change the filter part so its for videos
    all_rentals = db.session.query(Rental).join(Video, Video.video_id==Rental.video_id)\
        .join(Customer, Customer.customer_id==Rental.customer_id).filter(Video.video_id == video_id).all()

    list_of_rentals = []
    for rental in all_rentals:
        list_of_rentals.append({
            "due_date": rental.due_date,
            "name": Customer.query.get(rental.customer_id).name,
            "phone": Customer.query.get(rental.customer_id).phone,
            "postal_code": Customer.query.get(rental.customer_id).postal_code
        })
    return jsonify(list_of_rentals), 200