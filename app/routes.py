from flask import Blueprint, make_response, jsonify, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from datetime import datetime
import re


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

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
            is_valid_phone(request_body["phone"])
    ):
        return make_response({
            "errors": [
                "Bad Request",
                "'name' is required",
                "'postal_code' is required and should be a number",
                "'phone' is required and should be (XXX) XXX-XXXX"
            ]
        }, 400)

    new_customer = Customer()
    new_customer = new_customer.from_json(request_body)
    db.session.add(new_customer)
    db.session.commit()

    retrieve_customer = Customer.query.get(new_customer.customer_id)
    return make_response(retrieve_customer.to_json(), 201)


@ customers_bp.route("/<customer_id>", methods=["PUT"])
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
            is_valid_phone(request_body["phone"]) and
            # "registered_at" in request_body and
            # "videos_checked_out_count" in request_body and
            is_number(request_body["postal_code"])):

        return make_response({
            "errors": [
                "Bad Request",
                "'name' is required",
                "'postal_code' is required and should be a number",
                "'phone' is required and should be (XXX) XXX-XXXX"
                # "'registered_at' is required",
                # "'videos_checked_out_count' is required and should be a number"
            ]
        }, 400)

    customer = customer.from_json(request_body)
    db.session.commit()
    retrieve_customer = Customer.query.get(customer_id)

    return make_response(retrieve_customer.to_json(), 200)


@ customers_bp.route("/<customer_id>", methods=["DELETE"])
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


@ videos_bp.route("", methods=["GET"])
def get_all_videos():
    """Lists all existing videos and details about each video."""
    videos = Video.query.all()
    response = [video.to_json() for video in videos]
    return jsonify(response), 200


@ videos_bp.route("/<video_id>", methods=["GET"])
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


@ videos_bp.route("", methods=["POST"])
def add_video():
    """Creates a new video with the given Request Body Parameters."""
    request_body = request.get_json()

    if not (
            "title" in request_body and
            "release_date" in request_body and
            "total_inventory" in request_body and
            is_number(request_body["total_inventory"])):
        return make_response({
            "errors": [
                "Bad Request",
                "'title' is required",
                "'release_date' is required",
                "'total_inventory' is required and should be a number"
            ]
        }, 400)

    new_video = Video()
    new_video = new_video.from_json(request_body)
    new_video.available_inventory = new_video.total_inventory
    db.session.add(new_video)
    db.session.commit()

    retrieve_video = Video.query.get(new_video.video_id)
    return make_response(retrieve_video.to_json(), 201)


@ videos_bp.route("/<video_id>", methods=["PUT"])
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
            "title" in request_body and
            "release_date" in request_body and
            "total_inventory" in request_body and
            is_number(request_body["total_inventory"])):

        return make_response({
            "errors": [
                "Bad Request",
                "'title' is required",
                "'release_date' is required",
                "'total_inventory' is required and should be a number"
            ]
        }, 400)

    video = video.from_json(request_body)
    db.session.commit()
    retrieve_video = Video.query.get(video_id)

    return make_response(retrieve_video.to_json(), 200)


@ videos_bp.route("/<video_id>", methods=["DELETE"])
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

# -------------- Custom endpoints for /rentals ------------------------


@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video_to_customer():
    """Checks out a video to a customer, and updates the data in the database as such."""

    request_body = request.get_json()

    if not (
            "customer_id" in request_body and
            "video_id" in request_body and
            is_number(request_body["customer_id"]) and
            is_number(request_body["video_id"])):

        return make_response({
            "errors": [
                "Bad Request",
                "'customer_id' is required and should be a number",
                "'video_id' is required and should be a number"
            ]
        }, 400)

    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])

    if video is None or customer is None:
        return make_response({
            "errors": [
                "Not Found",
                "Customer does not exist",
                "Video does not exist"
            ]
        }, 404)

    if video.available_inventory <= 0:
        return make_response({
            "errors": [
                "Bad Request",
                "Video does not have any available inventory"
            ]
        }, 400)

    rental = Rental(
        customer_id=customer.customer_id,
        video_id=video.video_id
    )

    video.available_inventory -= 1
    customer.videos_checked_out_count += 1

    db.session.add_all([rental, video, customer])
    db.session.commit()

    # print(rental)

    # results = db.session.query(Customer, Video, Rental).join(
    #     Customer, Customer.customer_id == Rental.customer_id).join(
    #         Video, Video.video_id == Rental.video_id).filter(
    #             Customer.customer_id == request_body["customer_id"]).all()

    # print(results)

    return ({
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "due_date": rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }, 200)
