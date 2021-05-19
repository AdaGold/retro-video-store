from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

#################### Routes for Customers ####################
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customer():
    customers = Customer.query.all()
    customer_response = [customer.to_json() for customer in customers]
    return jsonify(customer_response), 200

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)  
def get_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return customer.to_json(), 200
    else:
        return jsonify(None), 404

@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customer_rentals(customer_id):
    # results = db.session.query(Customer, Video, Rental).join(Customer, Customer.customer_id==Rental.customer_id).join(Video, Video.video_id==Rental.video_id).filter(Customer.customer_id == customer_id).all()
    # print(results[0][1].to_json())
    customer = Customer.query.get(customer_id)
    print(customer.videos_rent[0].title)
    return jsonify(None), 200

@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False) 
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        form_data = request.get_json()
        if all(key in form_data for key in ("name", "postal_code", "phone")):
            customer.name = form_data["name"]
            customer.postal_code = form_data["postal_code"]
            customer.phone = form_data["phone"]
            db.session.commit()
            return customer.to_json(), 200
        else:
            return jsonify(None), 400
    else:
        return jsonify(None), 404
        
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    request_body = request.get_json()
    if all(key in request_body for key in ("name", "postal_code", "phone")):
        new_customer = Customer.from_json(request_body)
        new_customer.register_at = datetime.utcnow()
        db.session.add(new_customer)
        db.session.commit()
        return new_customer.to_json(), 201
    else:
        return {"details": "Invalid data"}, 400
      
@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return customer.to_json(), 200
    else:
        return jsonify(None), 404
      
#################### Routes for Videos ####################
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_video():
    videos = Video.query.all()
    video_response = [video.to_json() for video in videos]
    return jsonify(video_response), 200

@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)  
def get_single_customer(video_id):
    video = Video.query.get(video_id)
    if video:
        return video.to_json(), 200
    else:
        return jsonify(None), 404

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_video():
    request_body = request.get_json()
    if all(key in request_body for key in ("title", "release_date", "total_inventory")):
        new_video = Video.from_json(request_body)
        new_video.available_inventory = request_body["total_inventory"]
        db.session.add(new_video)
        db.session.commit()
        return new_video.to_json(), 201
    else:
        return {"details": "Invalid data"}, 400
      
@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False) 
def update_video(video_id):
    video = Video.query.get(video_id)
    if video:
        form_data = request.get_json()
        if all(key in form_data for key in ("title", "release_date", "total_inventory")):
            video.title = form_data["title"]
            video.release_date = form_data["release_date"]
            video.total_inventory = form_data["total_inventory"]
            db.session.commit()
            return video.to_json(), 200
        else:
            return jsonify(None), 400
    else:
        return jsonify(None), 404
      
@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video:
        db.session.delete(video)
        db.session.commit()
        return video.to_json(), 200
    else:
        return jsonify(None), 404
      
#################### Routes for Rentals ####################
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    new_rental = Rental.from_json(request_body)
    db.session.add(new_rental)
    customer = Customer.query.get(customer_id)
    customer.videos_checked_out_count += 1
    video = Video.query.get(video_id)
    video.available_inventory = video.total_inventory - 1
    db.session.commit()
    return {
          "customer_id": new_rental.customer_id,
          "video_id": new_rental.video_id,
          "due_date": datetime.utcnow() + timedelta(days=7),
          "videos_checked_out_count": customer.videos_checked_out_count,
          "available_inventory": video.available_inventory
    }, 200
    

