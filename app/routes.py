import requests
import os
from flask import request, Blueprint, make_response, jsonify

from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from datetime import datetime, timedelta 

# <------------------------------------- CUSTOMER ENDPOINTS ------------------------------------->

customers_bp = Blueprint("customers", __name__, url_prefix= "/customers")

# endpoint retrieves details about ALL customers and creates a record of a customer
@customers_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def customer_details():

    # GET all customer details 
    
    if request.method == "GET":

        all_customers = Customer.query.all()

        customers_response = []
        for customer in all_customers:
            customers_response.append({
                "id": customer.id,
                "name": customer.name,
                "registered_at": customer.registered_at,
                "postal_code": customer.postal_code,
                "phone": customer.phone,
                "videos_checked_out_count": customer.videos_checked_out_count
            })
        return jsonify(customers_response), 200
    
    # CREATES (POST) a new customer

    elif request.method == "POST":

        request_body = request.get_json()
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        else:
            new_customer = Customer(
                name=request_body["name"], 
                postal_code=request_body["postal_code"], 
                phone=request_body["phone"],
                registered_at=datetime.now()
                )

            db.session.add(new_customer)
            db.session.commit()

            return new_customer.to_json(), 201
        
# endpoint retrieves, updates and deletes records of a specific customer
@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def specific_customer(customer_id):

    # GET details about specific customer

    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response(), 404
    
    elif request.method == "GET":
        return customer.to_json(), 200

    # UPDATE (PUT) & return details about specific customer

    elif request.method == "PUT":
        form_data = request.get_json()

        if "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data:
            return jsonify({"details": "Invalid data"}), 400
        
        else:
            customer.name = form_data["name"]
            customer.postal_code = form_data["postal_code"]
            customer.phone = form_data["phone"]

            db.session.commit()
            return customer.to_json(), 200
    
    # DELETE a specific customer
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return jsonify({
            "id": customer.id,
            "details": f'Customer {customer.name} successfully deleted'}), 200


# <------------------------------------- VIDEO ENDPOINTS ------------------------------------->

videos_bp = Blueprint("videos", __name__, url_prefix= "/videos")

# endpoint retrieves details about ALL videos and creates a record of a video
@videos_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def video_details():

    # GET all existing videos and details about each video
    
    if request.method == "GET":

        all_videos = Video.query.all()

        videos_response = []
        for video in all_videos:
            videos_response.append({
                "id": video.id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory": video.total_inventory,
                "available_inventory": 0
            })
        
        return jsonify(videos_response), 200

    # CREATES (POST) a new VIDEO

    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        else:
            new_video = Video(
                title=request_body["title"], 
                release_date=request_body["release_date"], 
                total_inventory=request_body["total_inventory"],
                available_inventory=request_body["total_inventory"]
                )

            db.session.add(new_video)
            db.session.commit()

            return make_response({
                "id": new_video.id,
                "title": new_video.title
                }, 201) 

# endpoint retrieves, updates and deletes records of a specific video
@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def specific_video(video_id):

    # GET details about specific video

    video = Video.query.get(video_id)

    if video is None:
        return make_response(), 404
    
    elif request.method == "GET":
        return video.to_json(), 200

    # UPDATE (PUT) & return details about specific video

    elif request.method == "PUT":
        form_data = request.get_json()

        if "title" not in form_data or "release_date" not in form_data or "total_inventory" not in form_data:
            return jsonify({"details": "Invalid data"}), 400

        else:
            video.title = form_data["title"]
            video.release_date = form_data["release_date"]
            video.total_inventory = form_data["total_inventory"]
            db.session.commit()
            return video.to_json(), 200
    
    # DELETE a specific video
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

        return jsonify({
            "id": video.id,
            "details": f'Video {Video.title} successfully deleted'}), 200



# <------------------------------------- RENTAL ENDPOINTS ------------------------------------->

rentals_bp = Blueprint("rentals", __name__, url_prefix= "/rentals")
# POST /rentals/check-in -> checks out a video to a customer and updates the data in the db 
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def rental_check_out():
    request_body = request.get_json()

    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")

    if type(customer_id) != int or type(video_id) != int:
        return make_response({"details": "Invalid data"}), 400
    
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer is None and video is None:
        return make_response(), 404

    if video.available_inventory < 1:
        return jsonify({"details": "Invalid data"}), 400

    customer.videos_checked_out_count += 1
    video.available_inventory -= 1

    new_rental = Rental(
        customer_id=customer_id,
        video_id=video_id,
        due_date=datetime.now() + timedelta(days=7)
    )

    db.session.add(new_rental)
    db.session.commit()

    return jsonify({
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }), 200

# POST /rentals/check-in -> checks in a video to a customer and updates the data in the db
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def rental_check_in():
    request_body = request.get_json()

    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    for rental in customer.video:
        if rental.video_id == video_id:
            customer.videos_checked_out_count -= 1
            video.available_inventory += 1
            db.session.delete(rental)
            db.session.commit()
        
            return jsonify({
                "customer_id": customer_id,
                "video_id": video_id,
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory
            }), 200

    else:
        return jsonify({"details": "Invalid data"}), 400

# GET /customers/<id>/rentals -> list the videos a customer currently has checked out 
@customers_bp.route("<int:id>/rentals", methods=["GET"], strict_slashes=False)
def customer_rentals(id):
    customer = Customer.query.get(id)

    if customer is None:
        return jsonify({"details": "Invalid data"}), 404


    customer_rentals = []
    for rental in customer.video:
        video = Video.query.get(rental.video_id)

        customer_rentals.append({
            "release_date": video.release_date,
            "title": video.title,
            "due_date": datetime.now() + timedelta(days=7)
        })

    return jsonify(customer_rentals), 200

# GET /videos/<id>/rentals -> list the customers who currently have the video checked out
@videos_bp.route("<int:id>/rentals", methods=["GET"], strict_slashes=False)
def video_rentals(id):
    video = Video.query.get(id)

    if video is None:
        return jsonify({"details": "Invalid data"}), 404


    customer_details = []
    for rental in video.customer:
        customer = Customer.query.get(rental.customer_id)

        customer_details.append({
            "due_date": datetime.now() + timedelta(days=7),
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        })

        return jsonify(customer_details), 200
