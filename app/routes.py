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

####################### Blueprints ########################
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
welcome_page = Blueprint('welcome_page', __name__)

#################### Routes for Welcome page ####################
@welcome_page.route('/')
def index():
    return {
        "name": "Weishan Yang",
        "message": "Hi instructors! Welcome to the rainbow video store!"
    }

#################### Routes for Customers ####################
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
        return {"details": "Customer not found"}, 404

@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customer_rentals(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return {"details": "Customer not found"}, 404
    videos = customer.videos_rent
    response = []
    for video in videos:
        related_rental = Rental.query.filter_by(customer_id=customer_id, video_id=video.video_id).first() 
        detailed_info = {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": related_rental.due_date
        }
        response.append(detailed_info)
    return jsonify(response), 200

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
            return {"details": "Invalid data"}, 400
    else:
        return {"details": "Customer not found"}, 404
        
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
        return {"details": "Customer not found"}, 404
      
#################### Routes for Videos ####################
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
        return {"details": "Video not found"}, 404
      
@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False) 
def get_video_renters(video_id):
    video = Video.query.get(video_id)
    if not video:
        return {"details": "Video not found"}, 404
    else:
        customers = video.renters
        response = []
        for customer in customers:
            related_rental = Rental.query.filter_by(customer_id=customer.customer_id, video_id=video_id).first() 
            customer_info = {
                "due_date": related_rental.due_date,
                "name": customer.name,
                "phone": customer.phone,
                "postal_code": customer.postal_code,
            }
            response.append(customer_info)
        return jsonify(response), 200
              
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
            if video.total_inventory > int(form_data["total_inventory"]):
                difference = video.total_inventory - int(form_data["total_inventory"])
                video.available_inventory -= difference
            else:
                difference = int(form_data["total_inventory"]) - video.total_inventory
                video.available_inventory += difference
            # difference = video.total_inventory - int(form_data["total_inventory"])
            video.total_inventory = form_data["total_inventory"]
            video.available_inventory - difference
            db.session.commit()
            return video.to_json(), 200
        else:
            return {"details": "Invalid data"}, 400
    else:
        return {"details": "Video not found"}, 404
      
@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video:
        db.session.delete(video)
        db.session.commit()
        return video.to_json(), 200
    else:
        return {"details": "Video not found"}, 404
      
#################### Routes for Rentals ####################
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    if not is_int(customer_id) or not is_int(video_id):
        return {"details": "Invalid data"}, 400
    else:
        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)
        if not customer or not video:
            return {"details": "Rental information not found"}, 404
        if video.available_inventory == 0:
            return {"details": "Video not available"}, 400
        else:
            new_rental = Rental.from_json(request_body)
            new_rental.due_date = datetime.utcnow() + timedelta(days=7)
            db.session.add(new_rental)
            customer.videos_checked_out_count += 1
            video.available_inventory -= 1
            db.session.commit()
            return new_rental.to_json(customer, video), 200
def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False
      
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    rental = Rental.query.filter_by(customer_id=customer_id, video_id=video_id).first()
    if not customer or not video:
        return {"details": "Rental information not found"}, 404
    if not rental:
        return {"details": "Video already checked in"}, 400
    else:
        db.session.delete(rental)
        db.session.commit()
        customer.videos_checked_out_count -= 1
        video.available_inventory += 1
        db.session.commit()
        return {
            "customer_id": customer_id,
            "video_id": video_id,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.available_inventory
        }, 200
