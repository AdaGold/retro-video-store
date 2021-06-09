
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime, timedelta
import os


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# CUSTOMER

@customers_bp.route("", methods = ["GET"])
def customer_index():
    customers = Customer.query.all()
    customers_response = [customer.to_json() for customer in customers]
    return make_response(jsonify(customers_response), 200)

@customers_bp.route("", methods = ["POST"])
def customers():
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    else:
        new_customer = Customer(name=request_body["name"], 
                                postal_code=request_body["postal_code"],
                                phone=request_body["phone"])
        new_customer.registered_at = datetime.now()
        db.session.add(new_customer)
        db.session.commit()
        return make_response({"id": new_customer.id}, 201)

@customers_bp.route("/<id>", methods = ["GET"])
def get_one_customer(id):
    customer = Customer.query.get_or_404(id)
    return  make_response(customer.to_json(), 200)

@customers_bp.route("/<id>", methods = ["PUT"])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    request_body = request.get_json() 
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    else:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
        db.session.commit()
    return make_response(customer.to_json(), 200)

@customers_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)
    db.session.commit()

    return make_response({"id": customer.id}, 200)

@customers_bp.route("/<id>/rentals", methods = ["GET"])
def customer_rentals(id):
    customer = Customer.query.get_or_404(id) 
    customer_rentals = Rental.query.filter_by(customer_id =customer.id)
    customer_videos = []

    for rental in customer_rentals:
        video=Video.query.get_or_404(rental.video_id)
        customer_videos.append({
                    "release_date": video.release_date,
                    "title": video.title,
                    "due_date": rental.due_date})
    return jsonify(customer_videos), 200

# VIDEO

@videos_bp.route("", methods = ["GET"])
def video_index():
    videos = Video.query.all() 
    videos_response = [video.to_json() for video in videos] 
    return make_response(jsonify(videos_response), 200)

@videos_bp.route("", methods = ["POST"])
def videos():
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return make_response({"details": "Invalid data"}, 400)    
    else: 
        new_video = Video(title=request_body["title"], 
                        release_date=request_body["release_date"],
                        total_inventory=request_body["total_inventory"],
                        available_inventory=request_body["total_inventory"]) 
        db.session.add(new_video)
        db.session.commit() 
        return make_response({"id": new_video.id}, 201)

@videos_bp.route("/<id>", methods = ["GET"])
def get_one_video(id):
    video = Video.query.get_or_404(id)
    return  make_response(video.to_json(), 200)

@videos_bp.route("/<id>", methods = ["PUT"])
def update_video(id):
    video = Video.query.get_or_404(id)
    request_body = request.get_json() 
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return make_response({"details": "Invalid data"}, 400)    
    else:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
        db.session.commit()
    return make_response(video.to_json(), 200) 

@videos_bp.route("/<id>", methods = ["DELETE"])
def delete_video(id):
    video = Video.query.get_or_404(id)
    
    db.session.delete(video)
    db.session.commit()

    return make_response({"id": video.id}, 200)


@videos_bp.route("/<id>/rentals", methods = ["GET"])
def video_rentals(id): 
    video = Video.query.get_or_404(id)
    video_rentals = Rental.query.filter_by(video_id = video.id)
    customers_by_video = []
    for rental in video_rentals:
        customer=Customer.query.get_or_404(rental.customer_id)
        
        customers_by_video.append({
                        "due_date": rental.due_date,
                        "name": customer.name,
                        "phone": customer.phone,
                        "postal_code": str(customer.postal_code)})
    return jsonify(customers_by_video), 200


# RENTAL

@rentals_bp.route("/check-out", methods = ["POST"])
def check_out():
    request_body = request.get_json()
    customer_id = request_body.get("customer_id")
    video_id=request_body.get("video_id")

    customer = Customer.query.get_or_404(customer_id)
    video = Video.query.get_or_404(video_id)

    if video.available_inventory == 0: return make_response({"errors": "No video available"}, 400)

    customer.videos_checked_out_count += 1
    video.available_inventory -= 1
    
    rental = Rental(customer_id = customer.id, video_id=video.id, due_date = datetime.now() + timedelta(days=7))
    db.session.add(rental)
    db.session.commit() 

    return {
        "customer_id": customer.id,
        "video_id": video.id,
        "due_date": rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
                }, 200


@rentals_bp.route("/check-in", methods = ["POST"])
def check_in():
    request_body = request.get_json()
    customer_id = request_body.get("customer_id")
    video_id=request_body.get("video_id")

    customer = Customer.query.get_or_404(customer_id)
    video = Video.query.get_or_404(video_id)
    rental = Rental.query.filter_by(customer_id = customer_id, video_id = video_id).one_or_none()

    if not rental:
        return make_response({"details": "Invalid data"}, 400)

    customer.videos_checked_out_count -= 1
    video.available_inventory += 1
    db.session.delete(rental)
    db.session.commit()

    return jsonify({
        "customer_id": customer.id,
        "video_id": video.id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
        }), 200
