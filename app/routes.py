from app import db
import requests
from flask import request, Blueprint, make_response
from flask import jsonify
from app.models.customer import Customer
from app.models.video import Video
# from app.models.rental import Rental
from dotenv import load_dotenv
from datetime import datetime
import os


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
# rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")



@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_body = request.get_json()
    
    if ("name" not in request_body or "postal_code" not in request_body \
        or "phone" not in request_body):
        return jsonify({"erro":"Invalid data"}),400
    
    else:
        customer = Customer(name = request_body["name"],
                        postal_code = request_body["postal_code"],
                        phone = request_body["phone"],
                        registered_at = datetime.now())

    db.session.add(new_customer)
    db.session.commit()
    return jsonify({
        "id": customer.id
    }), 201
    

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers = Customer.query.all()
    
    customer_list = []
    for customer in customers:
        customers_response.append(customer_list.to_json())
    return jsonify(customer_list)


@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def retrieve_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer is None:
        return "Customer not found.", 404

    if request.method == "GET":
        return customer.to_json_customer()
    
    if request.method == "PUT":

        customer_data = request.get_json()

        if "name" not in customer_data or "postal_code" not in customer_data or "phone" not in customer_data:
            return jsonify({
                "details": "Invalid data.  No name, postal code, and/or phone."
            }), 400

        customer.name = customer_data["name"]
        customer.postal_code = customer_data["postal_code"]
        customer.phone_num = customer_data["phone"]

        db.session.commit()

        return customer.to_json_customer()
    
    if request.method == "DELETE":

        db.session.delete(customer)
        db.session.commit()

        return jsonify({
            "id": customer.id})



@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_single_video(video_id):

    video = Video.query.get(video_id)

    if request.method == "GET":
        if video is None:
            return make_response("", 404) 

        else:
            make_response(video.to_json(), 200)


@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_videos():

    videos = Video.query.all()
    videos_response = []

    if videos is None:
        return 404

    for video in videos:
        videos_response.append(video.to_json_video())

    return jsonify(videos_response)


@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_videos():

    request_body = request.get_json()

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return jsonify({
            "errors": "Not Found"
            }), 400
    
    video = Video(title= request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"],
        available_inventory = request_body['total_inventory'])

    db.session.add(video)
    db.session.commit()

    return jsonify({
        "id": video.id
    }), 201


@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):

    video = Video.query.get(video_id)
    form_data = request.get_json()

    if video: 

        if "title" in form_data.keys() or "release_date" in form_data.keys() or "total_inventory" in form_data.keys():
            
            video.title = form_data["title"]
            video.release_date = form_data["release_date"]
            video.total_inventory = form_data["total_inventory"]

            db.session.commit()
    
            updated_video = video.to_json_video()
            
            return jsonify(updated_video)

    else: 
        return make_response("", 404) 
        
    

@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_one_video(video_id):
    
    one_video = Video.query.get(video_id)

    if not single_video:
        return make_response({"details": f"No video with ID #{video_id}"}, 404)

    db.session.delete(single_video)
    db.session.commit()
    return make_response({"id": one_video.video_id}, 200) 




# @rental_bp.route("/check-out", methods = ["POST"])
# def checked_out():
#     request_body = request.get_json()

#     customer_id = request_body.get("customer_id")
#     video_id = request_body.get("video_id")
    
#     if type(customer_id) != int or type(video_id) != int:
#         return jsonify({"details": "Invalid data"}), 400

#     customer = Customer.query.get(customer_id)
#     video = Video.query.get(video_id)

#     if customer is None and video is None:
#         return jsonify({"details": "do not exist"}), 404

#     if video.available_inventory < 1:
#         return jsonify({"details": "Invalid data"}), 400


#     customer.videos_checked_out_count += 1
#     video.available_inventory -= 1

#     new_rental = Rental(
#         customer_id = customer_id,
#         video_id = video_id,
#         due_date = datetime.now() + timedelta(days = 7)
#     )

#     db.session.add(new_rental)
#     db.session.commit()

#     return jsonify({
#         "customer_id": new_rental.customer_id,
#         "video_id": new_rental.video_id,
#         "due_date": new_rental.due_date,
#         "videos_checked_out_count": customer.videos_checked_out_count,
#         "available_inventory": video.available_inventory
#     }), 200

