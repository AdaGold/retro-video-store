from flask import Blueprint, make_response, jsonify, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime
import re


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

# ----------------- helper functions ------------------------


def is_number(input):
    condition = isinstance(input, int) or isinstance(input, float)
    return True if condition else False


def is_valid_phone(input):
    """Validates the phone number pattern (908) 949-6758"""
    pattern = re.compile(r'\(\d{3}\) \d{3}-\d{4}')
    return re.match(pattern, input) is not None


# -------------- CRUD for /customers ------------------------


@customers_bp.route("", methods=["GET"])
def get_all_customers():
    """Lists all existing customers and details about each customer."""
    customers = Customer.query.all()
    response = [customer.to_json() for customer in customers]
    return jsonify(response), 200


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    """Gives back details about specific customer."""
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response({
            "errors": [
                "Not Found",
                "Customer does not exist"
            ]
        }, 404)
    return make_response(customer.to_json(), 200)


@customers_bp.route("", methods=["POST"])
def add_customer():
    """Creates a new customer with the given Request Body Parameters."""
    request_body = request.get_json()

    if not (
            "name" in request_body and
            "postal_code" in request_body and
            "phone" in request_body and
            is_number(request_body["postal_code"]) and
            is_valid_phone(request_body["phone"])):

        return make_response({
            "errors": [
                "Bad Request",
                "'name' is required",
                "'postal_code' is required and should be a number",
                "'phone' is required",
            ]
        }, 400)

    new_customer = Customer()
    new_customer = new_customer.from_json(request_body)
    db.session.add(new_customer)
    db.session.commit()

    retrieve_customer = Customer.query.get(new_customer)
    return make_response(retrieve_customer.to_json(), 201)


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer_by_id(customer_id):
    """Updates and returns details about specific customer."""
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response({
            "errors": [
                "Not Found",
                "Customer to update does not exist"
            ]
        }, 404)

    request_body = request.get_json()

    if not (
            "name" in request_body and
            "postal_code" in request_body and
            "phone" in request_body and
            "registered_at" in request_body and
            "videos_checked_out_count" in request_body and
            is_number(request_body["videos_checked_out_count"])):

        return make_response({
            "errors": [
                "Bad Request",
                "'name' is required",
                "'postal_code' is required",
                "'phone' is required",
                "'registered_at' is required",
                "'videos_checked_out_count' is required"
            ]
        }, 400)

    customer = customer.from_json(request_body)
    db.session.commit()
    retrieve_customer = Customer.query.get(customer_id)

    return make_response(retrieve_customer.to_json(), 200)


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id):
    """Deletes a specific customer."""
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response({
            "errors": [
                "Not Found",
                "Customer to delete does not exist"
            ]
        }, 404)

    db.session.delete(customer)
    db.session.commit()
    # return ({"id": customer_id, "details": 'Task has been successfully
    # deleted'}, 200)
    return ({"id": customer_id}, 200)

# -------------- CRUD for /videos ------------------------


@videos_bp.route("", methods=["GET"])
def get_all_videos():
    """Lists all existing videos and details about each video."""
    videos = Video.query.all()
    response = [video.to_json() for video in videos]
    return jsonify(response), 200


@videos_bp.route("", methods=["POST"])
def add_video():
    """Creates a new video with the given Request Body Parameters."""
    request_body = request.get_json()

    if not (
            "title" in request_body and "release_date" in request_body and "total_inventory" in request_body):
        return make_response({
            "errors": [
                "Bad Request",
                "'title' is required",
                "'release_date' is required",
                "'total_inventory' is required"
            ]
        }, 400)

    new_video = Video()
    new_video = new_video.from_json(request_body)
    db.session.add(new_video)
    db.session.commit()

    retrieve_video = Video.query.get(new_video)
    return make_response(retrieve_video.to_json(), 201)


@videos_bp.route("/<video_id>", methods=["GET"])
def get_video_by_id(video_id):
    """Gives back details about specific video."""
    video = Video.query.get(video_id)

    if video is None:
        return make_response({
            "errors": [
                "Not Found",
                "Video does not exist"
            ]
        }, 404)
    return make_response(video.to_json(), 200)


@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video_by_id(video_id):
    """Updates and returns details about specific video."""
    video = Video.query.get(video_id)

    if video is None:
        return make_response({
            "errors": [
                "Not Found",
                "Video to update does not exist"
            ]
        }, 404)

    request_body = request.get_json()

    if not (
        "total_inventory" in request_body and
        "available_inventory" in request_body and
        is_number(request_body["total_inventory"]) and
            is_number(request_body["available_inventory"])):

        return make_response({
            "errors": [
                "Bad Request",
                "'total_inventory' is required",
                "'available_inventory' is required"
            ]
        }, 400)

    video = video.from_json(request_body)
    db.session.commit()
    retrieve_video = video.query.get(video_id)

    return make_response(retrieve_video.to_json(), 200)


@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video_by_id(video_id):
    """Deletes a specific video."""
    video = Video.query.get(video_id)

    if video is None:
        return make_response({
            "errors": [
                "Not Found",
                "Video to delete does not exist"
            ]
        }, 404)

    db.session.delete(video)
    db.session.commit()
    # return ({"id": video_id, "details": 'Video has been successfully
    # deleted'}, 200)
    return ({"id": video_id}, 200)
