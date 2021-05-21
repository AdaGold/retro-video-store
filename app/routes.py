import re
from flask import request, Blueprint
from app import db
from flask import jsonify
from .models.customer import Customer
from .models.video import Video
from .models.rental import Rental

import requests
import os

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")


@customer_bp.route("", methods=["POST"], strict_slashes=False)
def add_customer():
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return jsonify({
        "details": "Invalid data"
        }), 400
    new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"])
    
    db.session.add(new_customer)
    db.session.commit()
    return new_customer.to_json(), 201

@customer_bp.route("", methods=["GET"], strict_slashes=False)
def customer_index():
    customers = Customer.query.all()
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_json())

    return jsonify(customer_response), 200

@customer_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return jsonify(customer.to_json()), 200
    return "", 404

@customer_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        request_body = request.get_json()
        if "name" in request_body and "postal_code" in request_body and "phone" in request_body:
            customer.name = request_body["name"]
            customer.postal_code = request_body["postal_code"]
            customer.phone = request_body["phone"]
            db.session.commit()
            updated_customer = customer.to_json()
            return jsonify(updated_customer), 200
        return jsonify({
        "details": "Invalid data"
        }), 400
    return "", 404
  
@customer_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({
        "id": customer.customer_id
        }), 200
    return "", 404

@video_bp.route("", methods=["POST"], strict_slashes=False)
def add_video():
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return jsonify({
        "details": "Invalid data"
        }), 400
    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"],
                    available_inventory= request_body["total_inventory"]
                    )
    
    db.session.add(new_video)
    db.session.commit()
    return jsonify({
        "id": new_video.video_id
    }), 201

@video_bp.route("", methods=["GET"], strict_slashes=False)
def video_index():
    videos = Video.query.all()
    video_response = []
    for video in videos:
        video_response.append(video.to_json())

    return jsonify(video_response), 200

@video_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_video(video_id):
    video = Video.query.get(video_id)
    if video:
        return jsonify(video.to_json()), 200
    return "", 404

@video_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):
    video = Video.query.get(video_id)
    if video:
        request_body = request.get_json()
        if "title" in request_body and "release_date" in request_body and "total_inventory" in request_body:
            video.title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory = request_body["total_inventory"]
            db.session.commit()
            updated_video = video.to_json()
            return jsonify(updated_video), 200
        return jsonify({
        "details": "Invalid data"
        }), 400
    return "", 404

@video_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video:
        db.session.delete(video)
        db.session.commit()
        return jsonify({
        "id": video.video_id
        }), 200
    return "", 404

@rental_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def add_rental():
    request_body = request.get_json()
    if "customer_id" not in request_body or "video_id" not in request_body:
        return jsonify({
        "details": "Invalid data"
        }), 400

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    try:
        customer = Customer.query.get(customer_id)
    except:
        return jsonify({
        "details": "no such customer exists"
        }), 400

    try:
        video = Video.query.get(video_id)
    except:
        return jsonify({
        "details": "no such video exists"
        }), 400

    customer.videos_checked_out_count += 1
    if video.available_inventory < 1:
        return jsonify({
        "details": "not enough inventory available. hehe"
        }), 400
    video.available_inventory -= 1

    new_rental = Rental(customer_id=request_body["customer_id"],
                            video_id=request_body["video_id"])
    
    db.session.add(new_rental)
    db.session.commit()
    return jsonify({
        "customer_id": new_rental.customer_id,
        "video_id" : new_rental.video_id,
        "due_date" : new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
        }), 200


@rental_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def remove_rental():
    request_body = request.get_json()
    if "customer_id" not in request_body or "video_id" not in request_body:
                    return jsonify({
                    "details": "Invalid data"
                    }), 400

    customer_id_request = request_body["customer_id"]
    results = db.session.query(Customer, Video, Rental).join(Customer, Customer.customer_id==Rental.customer_id)\
        .join(Video, Video.video_id==Rental.video_id).filter(Customer.customer_id == customer_id_request).all()

    if len(results) < 1:
        return jsonify({
        "details": "so such rental exists"
        }), 400

    customer = results[0][0]
    video = results[0][1]
    query_rental = results[0][2]

    customer.videos_checked_out_count -= 1
    video.available_inventory += 1
    db.session.delete(query_rental)
    db.session.commit()
    return jsonify({
        "customer_id": customer.customer_id,
        "video_id" : video.video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
        }), 200

@customer_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_rentals_by_id(customer_id):
    rentals = db.session.query(Customer, Video, Rental).join(Customer, Customer.customer_id==Rental.customer_id)\
        .join(Video, Video.video_id==Rental.video_id).filter(Customer.customer_id == customer_id).all()

    customer = rentals[0][0]
    video = rentals[0][1]
    rentals = rentals[0][2]

    rental_response = []
    rental_response = [{
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rentals.due_date
            }]
    return jsonify(rental_response), 200

@video_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_rentals_by_video_id(video_id):
    rentals = db.session.query(Customer, Video, Rental).join(Customer, Customer.customer_id==Rental.customer_id)\
        .join(Video, Video.video_id==Rental.video_id).filter(Video.video_id == video_id).all()

    customer = rentals[0][0]
    rentals = rentals[0][2]

    rental_response = [{
            "due_date": rentals.due_date,
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
            }]
    return jsonify(rental_response), 200