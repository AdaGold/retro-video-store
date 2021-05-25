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
        customer = Customer.query.get(customer_id)
        # Getting videos_checked_out_count from customer object/class with the .
        customer.videos_checked_out_count += 1
        
        video_id=request_body["video_id"]
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
