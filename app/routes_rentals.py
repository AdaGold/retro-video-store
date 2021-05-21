from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer
from flask import Blueprint, request, jsonify, make_response
from app import db
from datetime import datetime

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out_rentals(): 
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if type(customer_id) != int or type(video_id) != int: 
        return {"details": "Invalid customer id or video id"}, 400
    
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer and video: 
        if video.available_inventory == 0: 
            return {"details": "insufficient inventory"}, 400
        else:
            new_rental = Rental.make_a_rental(request_body, id=None)
            customer.videos_checked_out_count += 1
            video.available_inventory -= 1
            
            db.session.add(new_rental)
            db.session.commit()

            return jsonify(new_rental.check_out_to_json(customer, video)), 200

    return make_response("", 404)

@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in_rentals(): 
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if type(customer_id) != int or type(video_id) != int: 
        return {"details": "Invalid customer id or video id"}, 400
    
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer and video: 
        rental = Rental.query.filter_by(customer_id=customer_id, video_id=video_id).all()
        if rental: 
            customer.videos_checked_out_count -= 1
            video.available_inventory += 1
            
            for rental in rental:
                db.session.delete(rental)
            db.session.commit()

            return {
                    "customer_id": customer_id,
                    "video_id": video_id,
                    "videos_checked_out_count": max(0,customer.videos_checked_out_count),
                    "available_inventory": video.available_inventory            
            }, 200
        return {"details": "this rental record does not exist"}, 400
    return make_response("", 404)