from app import db
from .models.video import Video
from .models.customer import Customer
from .models.rental import Rental
from .helpers import dict_helper
from flask import request, Blueprint, make_response, jsonify
from sqlalchemy import desc, asc
import datetime
import calendar
import os
from dotenv import load_dotenv
import requests

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@customer_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customer_list = [customer.cust_details() for customer in customers]

    return jsonify(customer_list), 200

@customer_bp.route("", methods=["POST"])
def create_new_customer():
    request_body = request.get_json()
    # if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
    keys = ["name", "postal_code", "phone"]
    if dict_helper.missing_any(request_body, keys):
        return jsonify({"errors": "Invalid data"}), 400      

    new_customer = Customer(name = request_body["name"],
    registered_at = datetime.datetime.now(),
    postal_code = request_body["postal_code"],
    phone = request_body["phone"],
    videos_checked_out_count = 0)
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"id": new_customer.customer_id}), 201

@customer_bp.route("/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return jsonify({"error": "Invalid data"}), 404

    return jsonify(customer.cust_details()), 200

@customer_bp.route("/<customer_id>", methods=["PUT"])
def put_by_customer_id(customer_id):
    customer = Customer.query.get(customer_id)
    form_data = request.get_json()

    if not customer:
        return jsonify({"errors": "Customer not found"}), 404
    if not form_data:
        return jsonify({"errors": "Invalid data"}), 400

    customer.name = form_data['name']
    customer.postal_code = form_data['postal_code']
    customer.phone = form_data['phone']
    db.session.commit()

    return jsonify(customer.cust_details()), 200

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return jsonify({"errors": "Customer not found"}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"id": customer.customer_id}), 200

@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    video_list = [video.vid_details() for video in videos]

    return jsonify(video_list), 200

@video_bp.route("", methods=["POST"])
def create_new_video():
    request_body = request.get_json()
    keys = ["title", "release_date", "total_inventory"]
    if dict_helper.missing_any(request_body, keys):
            return jsonify({"errors": "Invalid data"}), 400      

    new_video = Video(title = request_body["title"],
    release_date = request_body["release_date"],
    total_inventory = request_body["total_inventory"],
    available_inventory = request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit()

    return jsonify({"id": new_video.video_id}), 201

@video_bp.route("/<video_id>", methods=["GET"])
def get_video_by_id(video_id):
    video = Video.query.get(video_id)
    if video == None:
        return jsonify({"error": "Invalid data"}), 404
    
    return jsonify(video.vid_details()), 200

@video_bp.route("/<video_id>", methods=["PUT"])
def put_by_video_id(video_id):
    video = Video.query.get(video_id)
    form_data = request.get_json()
    if video == None:
        return jsonify({"errors": "Video not found"}), 404
    if form_data == {}:
        return jsonify({"errors": "Invalid data"}), 400

    video.title = form_data['title']
    video.release_date = form_data['release_date']
    video.total_inventory = form_data['total_inventory']
    db.session.commit()
    return jsonify(video.vid_details()), 200

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video == None:
        return jsonify({"errors": "Video not found"}), 404

    db.session.delete(video)
    db.session.commit()
    return jsonify({"id": video.video_id}), 200

@rental_bp.route("/check-out", methods = ["POST"])
def check_out_video():
    request_body = request.get_json()
    if "video_id" not in request_body or "customer_id" not in request_body:
        return jsonify({"errors": "Invalid data."}), 400
    if not isinstance(request_body["video_id"], int) or not isinstance(request_body["customer_id"], int):
        return jsonify({"errors": "Invalid data."}), 400

    vid_id = request_body["video_id"]
    cust_id = request_body["customer_id"]
    video = Video.query.get(vid_id)
    customer = Customer.query.get(cust_id)

    if video == None or customer == None:
        return jsonify({"error": "Invalid data."}), 404
    if video.available_inventory == 0:
        return jsonify({"error": "Out of stock."}), 400
    if video.available_inventory == 0:
        return jsonify({"error": "Out of stock."}), 400

    video.check_out()
    customer.check_out()

    new_rental = Rental(
    video_id = request_body["video_id"],
    customer_id = request_body["customer_id"],
    due_date = datetime.datetime.now()+datetime.timedelta(days=7))

    db.session.add(new_rental)
    db.session.commit()

    return jsonify({
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
        }), 200

@rental_bp.route("/check-in", methods = ["POST"])
def check_in_video():
    request_body = request.get_json()
    vid_id = request_body["video_id"]
    cust_id = request_body["customer_id"]
    video = Video.query.get(vid_id)
    customer = Customer.query.get(cust_id)
    check_if_rental = Rental.query.filter_by(video_id=vid_id, customer_id=cust_id).all()
    

    if "video_id" not in request_body or "customer_id" not in request_body:
        return jsonify({"errors": "Invalid data."}), 400
    if not isinstance(request_body["video_id"], int) or not isinstance(request_body["customer_id"], int):
        return jsonify({"errors": "Invalid data."}), 400
    if video == None or customer == None:
        return jsonify({"error": "Invalid data."}), 404
    if len(check_if_rental) == 0:
        return jsonify({"error": "Invalid data."}), 400

    
    video.check_in()
    customer.check_in()
    db.session.commit()

    rental_return = {
        "customer_id": cust_id,
        "video_id": vid_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
        }

    rental = check_if_rental[0]    
    db.session.delete(rental)
    db.session.commit()

    return jsonify(rental_return), 200

@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_rentals_by_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)
    # if customer == None:
    if not customer:
        return jsonify({"error": "Invalid data"}), 404
    customer_rentals = Rental.query.filter_by(customer_id=customer_id).all()

    video_ids = []
    due_dates = []
    titles = []
    videos = []
    release_dates = []
    for rental in customer_rentals:
        video_ids.append(rental.video_id)
        due_dates.append(rental.due_date)
    for id in video_ids:
        videos.append(Video.query.get(id))
    # videos = Video.query.where(id.in_(video_ids))
    #way to query/filter without using a loop? optimizes so as to not overload/crash database
    for video in videos:
        release_dates.append(video.release_date)
        titles.append(video.title)
    
    video_return = []
    for i in range(len(video_ids)):
        video = {
            "release_date": release_dates[i],
            "title": titles[i],
            "due_date": due_dates[i]
        }
        video_return.append(video)

    return jsonify(video_return), 200

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def get_rentals_by_video(video_id):
    video = Video.query.get(video_id)
    if not video:
        return jsonify({"error": "Invalid data"}), 404
    
    video_rentals = Rental.query.filter_by(video_id=video_id).all()

    customer_ids = []
    due_dates = []
    customers = []
    phone = []
    name = []
    postal = []
    for rental in video_rentals:
        customer_ids.append(rental.customer_id)
        due_dates.append(rental.due_date)
    for id in customer_ids:
        customers.append(Customer.query.get(id))
    for customer in customers:
        phone.append(customer.phone)
        name.append(customer.name)
        postal.append(customer.postal_code)
        
    
    rental_return = []
    for i in range(len(customer_ids)):
        rental ={
        "due_date": due_dates[i],
        "name": name[i],
        "phone": phone[i],
        "postal_code": postal[i]}

        rental_return.append(rental)
        
    return jsonify(rental_return), 200



        