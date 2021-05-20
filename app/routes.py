from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import Blueprint, jsonify, request, make_response
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers_index():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_json())
        
    return jsonify(customers_response), 200

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer_by_id():
    pass

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def add_customer():
    pass

@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_video():
    pass

@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer():
    pass


def videos_index():
    videos = Customer.query.all()
    videos_response = []
    for video in videos:
        videos_response.append(video.to_json())
        
    return jsonify(videos_response), 200

@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_video_by_id():
    pass

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def new_video():
    pass

@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video():
    pass

@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video():
    pass