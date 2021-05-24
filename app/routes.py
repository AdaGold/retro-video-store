from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
import os
import requests
from datetime import datetime, timedelta

now=datetime.now()

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")
video_bp = Blueprint("video", __name__, url_prefix="/videos")
rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def get_rentals_by_video(video_id):

    rentals = db.session.query(Rental).filter(Rental.video_id ==video_id)

    if rentals is None:
        return jsonify(None), 404

    elif request.method == "GET":
        response = []

        for rental in rentals:

            customer = Customer.query.get(rental.customer_id)

            response.append({
                "due_date": rental.due_date,
                "name": customer.name,
                "phone": customer.phone,
                "postal_code": customer.postal_code
            })

        return jsonify(response), 200


@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_rentals_by_customer(customer_id):

    rentals = db.session.query(Rental).filter(Rental.customer_id ==customer_id)

    if rentals is None:
        return jsonify(None), 404

    elif request.method == "GET":
        response = []

        for rental in rentals:

            video = Video.query.get(rental.video_id)

            response.append({
                "release_date": video.release_date,
                "title": video.title,
                "due_date": rental.due_date
            })

        return jsonify(response), 200

@rental_bp.route("/check-in", methods=["POST"])
def return_video():
    if request.method == "POST":

        request_body = request.get_json()

        if request_body["customer_id"] and request_body["video_id"]:
            
            returned_rental = Rental(customer_id=request_body["customer_id"],
                                video_id=request_body["video_id"])

            customer = Customer.query.get(request_body["customer_id"])
            video = Video.query.get(request_body["video_id"])

            if not customer or not video:
                response = "Not found tho"
                return jsonify(response), 404

            elif customer.videos_checked_out_count != 0:

                customer.videos_checked_out_count -= 1
                video.available_inventory += 1

                db.session.commit()

                response = {"customer_id": returned_rental.customer_id,
                            "video_id": returned_rental.video_id,
                            "videos_checked_out_count": customer.videos_checked_out_count,
                            "available_inventory": video.available_inventory}
                
                return jsonify(response), 200
            
            else:
                response = "No available inventory"
            return jsonify(response), 400

        else:
            response = "Must include name_id and video_id"
            return jsonify(response), 400


@rental_bp.route("/check-out", methods=["POST"])
def rent_video():

    request_body = request.get_json()

    if type(request_body["customer_id"]) != int or type(request_body["video_id"]) != int:
        return jsonify(None), 400

    elif request_body["customer_id"] and request_body["video_id"]:
        
        new_rental = Rental(customer_id=request_body["customer_id"],
                            video_id=request_body["video_id"],
                            due_date = now + timedelta(7))

        customer = Customer.query.get(request_body["customer_id"])
        video = Video.query.get(request_body["video_id"])

        if not customer or not video:
            response = "Not found tho"
            return jsonify(response), 404

        elif video.available_inventory != 0:

            customer.videos_checked_out_count += 1
            video.available_inventory -= 1

            db.session.add(new_rental)
            db.session.commit()

            response = {"customer_id": new_rental.customer_id,
                        "video_id": new_rental.video_id,
                        "due_date": new_rental.due_date,
                        "videos_checked_out_count": customer.videos_checked_out_count,
                        "available_inventory": video.available_inventory}
            
            return jsonify(response), 200
        
        else:
            response = "No available inventory"
        return jsonify(response), 400

    else:
        response = "Must include name_id and video_id"
        return jsonify(response), 400


@customer_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def handle_customer():

    if request.method == "GET":

        customers = Customer.query.all()
        response = []

        if not customers:
            return jsonify(response), 200

        for customer in customers:
            response.append({
                "id": customer.customer_id,
                "name": customer.name,
                "postal_code": customer.postal_code,
                "phone": customer.phone,
                "registered_at": customer.registered_at,
                "videos_checked_out_count": customer.videos_checked_out_count
            })
        
        return jsonify(response), 200
    
    elif request.method == "POST":

        request_body = request.get_json()

        if all(key in request_body for key in ("name", "postal_code", "phone")):
            new_customer = Customer(name=request_body["name"], 
                                    postal_code=request_body["postal_code"],
                                    phone=request_body["phone"],
                                    registered_at=now)

            db.session.add(new_customer)
            db.session.commit()

            response = new_customer.json_response()

            return jsonify(response), 201
        
        else: 
            response = {"details": "Invalid data"}
            return jsonify(response), 400

@customer_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"])
def get_one_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404
        
    elif request.method == "GET":

        response = customer.json_response()

        return jsonify(response)

    elif request.method == "PUT":

        form_data = request.get_json()

        try:

            customer.name = form_data["name"]
            customer.postal_code = form_data["postal_code"]
            customer.phone=form_data["phone"]

            db.session.commit()

            response = customer.json_response()

            return jsonify(response), 200

        except:

            response = "Invalid request"
            
            return jsonify(response), 400
    
    elif request.method == "DELETE":

        db.session.delete(customer)
        db.session.commit()
        
        response = {"id": customer.customer_id}

        return jsonify(response), 200 

@video_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def handle_video():

    if request.method == "GET":

        videos = Video.query.all()
        response = []

        if not videos:
            return jsonify(response), 200

        for video in videos:
            response.append({
                "id": video.video_id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory": video.total_inventory
            })
        
        return jsonify(response), 200
    
    elif request.method == "POST":

        request_body = request.get_json()

        if all(key in request_body for key in ("title", "release_date", "total_inventory")):
            new_video = Video(title=request_body["title"],
                            release_date=request_body["release_date"],
                            total_inventory=request_body["total_inventory"])

            db.session.add(new_video)
            db.session.commit()

            response = new_video.json_response()

            return jsonify(response), 201
        
        else: 
            response = {"details": "Invalid data"}
            return jsonify(response), 400 


@video_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def get_one_video(video_id):

    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404
        
    elif request.method == "GET":

        response = video.json_response()

        return jsonify(response)

    elif request.method == "PUT":

        form_data = request.get_json()

        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

        db.session.commit()

        response = video.json_response()

        return jsonify(response), 200
    
    elif request.method == "DELETE":

        db.session.delete(video)
        db.session.commit()
        
        response = {"id": video.video_id}

        return jsonify(response), 200
