from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime
import requests
import json


# creates a new varible  to help create my new endpoint
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
# /rentals/check-out The @rental_bp.route is create from ^^^


@rental_bp.route("/check-out", methods=["POST"], strict_slashes=False)
# <check-out> would mean I have a parameter that will change since I dont want my parameter I dont add it to my function and I leave the bracket off
def check_out_video():
    if request.method == "POST":

        request_body = request.get_json()

        if "customer_id" not in request_body or "video_id" not in request_body:
            return make_response({
                "details": "Invaild data"
            }), 400

        customer_id = request_body["customer_id"]
        if isinstance(customer_id, int) is not True:
            return make_response({
                "details": "Invaild data"
            }), 400
        customer = Customer.query.get(customer_id)
        # Getting videos_checked_out_count from customer object/class with the .
        customer.videos_checked_out_count += 1

        video_id = request_body["video_id"]
        if isinstance(video_id, int) is not True:
            return make_response({
                "details": "Invaild data"
            }), 400
        video = Video.query.get(video_id)

        video.available_inventory -= 1
        if video.available_inventory < 0:
            return make_response({
                "details": "Invaild data"
            }), 400
        check_out_video_rental = Rental(
            customer_id=customer_id,
            video_id=request_body["video_id"])

        db.session.add(check_out_video_rental)
        db.session.commit()

        return make_response(check_out_video_rental.json_object(), 200)


@rental_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in_video():
    # This say the in my code request body is equal to JSON infor being passed in the test Enviroment.
    request_body = request.get_json()
    # this says if the request body dosen't have customer_ id and video_id it not enough info for the search to finish  making the details entered invaild.
    if "customer_id" not in request_body or "video_id" not in request_body:
        return make_response({
            "details": "Invaild data"
        }), 400

    customer_id = request_body["customer_id"]
    customer = Customer.query.get(customer_id)

    # decrease the customer's videos_checked_in_count by one.
    customer.videos_checked_out_count -= 1

    video_id = request_body["video_id"]
    video = Video.query.get(video_id)
    # increase the video's available_inventory by one.
    video.available_inventory += 1

    if customer.videos_checked_out_count < 0:
        return make_response({
            "details": "Invaild data"
        }), 400

    check_in_video_rental = Rental(
        customer_id=customer_id,
        video_id=request_body["video_id"])

    db.session.add(check_in_video_rental)
    db.session.commit()

    return make_response(check_in_video_rental.check_in_json_object(), 200)

# {
#     "customer_id": 21,
#     "video_id": 23,
#     "due_date": "Mon, 31 May 2021 23:52:26 GMT",
#     "videos_checked_out_count": 0,
#     "available_inventory": 1
# }
