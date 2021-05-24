from flask import Blueprint, request, make_response, jsonify
from app import db 
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from dotenv import load_dotenv
from datetime import datetime, timedelta

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
load_dotenv()


@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def new_rental():

    # create instance of rental using customer_id and video_id
    request_body = request.get_json()
    rental = Rental(customer_id=request_body["customer_id"], video_id=request_body["video_id"])

    # invalid customer input
    if type(request_body["customer_id"]) is not int:
        return {"Error": "Invalid customer input"}, 400

    # invalid video input
    if type(request_body["video_id"]) is not int:
        return {"Error": "Invalid video input"}, 400

    # get customer_id and create customer instance
    customer = Customer.query.get(rental.customer_id)

    # get video_id and create video instance
    video = Video.query.get(rental.video_id)

    # if customer and video exist
    if customer:

        # increase customer.videos_checked_out by 1
        customer.videos_checked_out += 1
    
        # decrease videos.total_inventory by 1
        if video.total_inventory != 0:
            video.total_inventory -= 1
        else:
            return {"Error": "Available inventory is not sufficient"}, 400
    
    else:
        return {"Error": "Customer does not exist"}, 404

    # add it to database and commit
    db.session.add(rental)
    db.session.commit()

    return {
        "customer_id": rental.customer_id,
        "video_id": rental.video_id,
        "due_date": rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out,
        "available_inventory": video.total_inventory
    }

@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def return_rental():

    # create instance of rental using customer_id and video_id
    request_body = request.get_json()
    rental = Rental(customer_id=request_body["customer_id"], video_id=request_body["video_id"])

    # add it to database and commit 
    # db.session.add(rental)
    # db.session.commit()

    # get customer_id and create customer instance
    customer = Customer.query.get(rental.customer_id)

    # get video_id and create video instance
    video = Video.query.get(rental.video_id)

    # if customer exists and is valid 
    if customer:

        # decreases customer.videos_checked_out by 1
        customer.videos_checked_out -= 1

    else:
        return {"Error": "Customer does not exist"}, 404

    # if video exists and is valid
    if video: 
        
        # increases videos.total_inventory by 1
        video.total_inventory += 1
    else:
        return {"Error": "Video does not exist"}, 404

    # add it to database and commit
    db.session.commit()

    return {
        "customer_id": rental.customer_id,
        "video_id": rental.video_id,
        "videos_checked_out_count": customer.videos_checked_out,
        "available_inventory": video.total_inventory
    }

