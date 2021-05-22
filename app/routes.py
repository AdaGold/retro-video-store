from flask import Blueprint
from .models.customer import Customer
from .models.video import Video
from .models.rental import Rental
from app import db
from flask import request, make_response, jsonify, Response
from datetime import datetime, timedelta
from sqlalchemy import desc, asc
import os
import requests

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False


####### CUSTOMER CRUD #########

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers = Customer.query.all()
    
    customers_response = []
    for customer in customers:
        customers_response.append(customer.customer_to_json())
    return jsonify(customers_response), 200

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_single_customer(customer_id):

    if not is_int(customer_id):
        return {
            "message": f"ID {customer_id} must be an integer",
            "success": False
        }, 400

    customer = Customer.query.get(customer_id)

    if customer is not None:
        return jsonify({"customer": customer.customer_to_json()}), 200
    else:
        return Response("This customer is not in our database!",status=404)
        


@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_body = request.get_json()
    
    if ("name" not in request_body or "postal_code" not in request_body \
        or "phone" not in request_body):
        return jsonify({"details":"Invalid data"}),400
    
    else:
        new_customer = Customer(name = request_body["name"],
                        postal_code = request_body["postal_code"],
                        phone = request_body["phone"])

    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"customer": new_customer.customer_to_json()}), 201


@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    request_body = request.get_json()
    customer = Customer.query.get(customer_id)
    
    if customer == None:
        return Response("This customer is not in our database!", status=404)

    elif ("name" not in request_body or "postal_code" not in request_body \
    or "phone" not in request_body):
        
        return jsonify({"details":"Invalid data"}),400
    
    elif customer: 
        form_data = request.get_json()

        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]
        customer.registered_at = form_data["registered_at"]

        db.session.commit()
        return jsonify({"customer": customer.customer_to_json()}), 200


@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)    
def delete_single_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer:
        db.session.delete(customer)
        db.session.commit()
        return {
            "details": f"customer {customer.customer_id} \"{customer.name}\" successfully deleted"}, 200
    
    elif customer == None:
        return Response("This customer is not in our database!", status=404)



####### VIDEO CRUD #########

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_videos():

#WAVE 3    
    sort_by_name = request.args.get("sort")
    if sort_by_name == "asc":
            videos = Video.query.order_by(Video.name.asc()).all()
    elif sort_by_name == "desc":
            videos = Video.query.order_by(Video.name.desc()).all()
    else:
        videos = Video.query.all()
    
    videos_response = []
    for video in videos:
        videos_response.append(video.video_to_json())

    return jsonify(videos_response), 200


@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_single_video(video_id):

    if not is_int(video_id):
        return {
            "message": f"ID {video_id} must be an integer",
            "success": False
        }, 400

    video = Video.query.get(video_id)

    if video is not None:
        return jsonify({"video": video.video_to_json()}), 200
    else:
        return Response("This video is not in our database!",status=404)


@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_video():
    request_body = request.get_json()

    if ("title" not in request_body or "release_date" not in request_body \
        or "total_inventory" not in request_body):
        return jsonify({"details":"Invalid data"}),400
    
    else:
        new_video = Video(title = request_body ["title"],
                        release_date = request_body["release_date"],
                        total_inventory = request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit()
    return jsonify({"video": new_video.video_to_json()}), 201

    
@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):
    request_body = request.get_json()
    video = Video.query.get(video_id)
    
    if video == None:
        return Response("This video is not in our database!", status=404)

    elif ("title" not in request_body or "release_date" not in request_body \
        or "total_inventory" not in request_body or "available_inventory" not in request_body):
        
        return jsonify({"details":"Invalid data"}),400
    
    elif video: 
        form_data = request.get_json()

        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]
        video.available_inventory = form_data["available_inventory"]

        db.session.commit()
        return jsonify({"video": video.video_to_json()}), 200


@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)    
def delete_single_video(video_id):
    video = Video.query.get(video_id)

    if video:
        db.session.delete(video)
        db.session.commit()
        return {
            "details": f"video {video.video_id} \"{video.title}\" successfully deleted"},200

    elif video == None:
        return Response("This video is not in our database!", status=404)


####### RENTALS CRUD #########

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out_video():
    
    request_body = request.get_json()

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if ("customer_id" not in request_body or "video_id" not in request_body):    
        return jsonify({"details":"Invalid data, incorrect customer ID or video ID!"}),400

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if video == None:
        return Response("This video is not in our database!", status=404)

    if customer == None:
        return Response("This customer is not in our database!", status=404)
        
    if video.available_inventory == 0:
        return jsonify({"details":"This video is not available right now!"}),400

    due_date = ((datetime.today()) + (timedelta(days=7)))
    new_rental = Rental(customer_id=customer_id, 
                        video_id=video_id, 
                        due_date=due_date)
    
    db.session.add(new_rental)
    db.session.commit()
    
    return jsonify({"rental": new_rental.rental_to_json()}), 200

@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in_video():
    
    request_body = request.get_json()

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if ("customer_id" not in request_body or "video_id" not in request_body):    
        return jsonify({"details":"Invalid data, incorrect customer ID or video ID!"}),400

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    rental = Rental.query.filter_by(customer_id=customer_id, video_id=video_id).first()

    if video == None:
        return Response("This video is not in the database!", status=404)

    if customer == None:
        return Response("This customer is not in the database!", status=404)

    if rental == None:
        return Response("This video is not in the rentals!", status=404)
    
    db.session.delete(rental)
    db.session.commit()
    
    return jsonify({"rental": rental.rental_to_json()}), 200

@videos_bp.route('<video_id>/rentals', methods=["GET"], strict_slashes=False)
def get_video_rentals(video_id):
    video = Video.get_video_by_id(video_id)

    if video == None:
        return Response("This video is not in the database!", status=404)

    video_rentals = []
    for rental in video.rentals:
        customer = Customer.query.get(rental.customer_id)
        video_rentals.append({
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code,
            "due_date": rental.due_date
        })
        return jsonify(video_rentals), 200

