from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from datetime import datetime
import os 
from dotenv import load_dotenv

load_dotenv()

# ===== Customers ===================================================
customers_bp = Blueprint("customer", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])

@customers_bp.route("", methods=["POST"])
def post_customers():
    request_body = request.get_json()
    try:
        new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
            register_at=datetime.now()
        )
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.to_dict(), 201)

@customers_bp.route("/<active_id>", methods=["GET"])
def get_customer(active_id):
    customer = Customer.query.get_or_404(active_id)
    return make_response(customer.to_dict(), 200)

@customers_bp.route("/<active_id>", methods=["PUT"])
def put_customer(active_id):
    customer = Customer.query.get_or_404(active_id)
    request_body = request.get_json()
    try:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    db.session.commit()
    return make_response(customer.to_dict(), 200)

@customers_bp.route("/<active_id>", methods=["DELETE"])
def delete_customer(active_id):
    customer = Customer.query.get_or_404(active_id)
    db.session.delete(customer)
    db.session.commit()
    return ({"id" : int(active_id)}, 200)

# ===== Videos ======================================================
videos_bp = Blueprint("video", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])

@videos_bp.route("", methods=["POST"])
def post_videos():
    request_body = request.get_json()
    try:
        new_video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"]
        )
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    db.session.add(new_video)
    db.session.commit()

    return make_response(new_video.to_dict(), 201)

@videos_bp.route("/<active_id>", methods=["GET"])
def get_video(active_id):
    video = Video.query.get_or_404(active_id)
    return make_response(video.to_dict(), 200)

@videos_bp.route("/<active_id>", methods=["PUT"])
def put_video(active_id):
    video = Video.query.get_or_404(active_id)
    request_body = request.get_json()

    try:
        video.title=request_body["title"],
        video.release_date=request_body["release_date"],
        video.total_inventory=request_body["total_inventory"]
    except KeyError:
        return make_response({"details" : "Invalid data"}, 400)

    db.session.commit()
    return make_response(video.to_dict(), 200)

@videos_bp.route("/<active_id>", methods=["DELETE"])
def delete_video(active_id):
    video = Video.query.get_or_404(active_id)
    db.session.delete(video)
    db.session.commit()
    return ({"id" : int(active_id)}, 200)

# ===== Rentals =====================================================