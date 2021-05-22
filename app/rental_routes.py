from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rental_bp.route("/check-out", methods=["POST"])  # strict_slashes=False??
def rental_check_out():
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        return {
            "details": f"Not found"
        }, 400

    customer = Customer.query.get(request_body.customer_id)
    if customer == None:
        return make_response(f"Customer {request_body.customer_id} not found", 404)

    video = Video.query.get(request_body.video_id)
    if video == None:
        return make_response(f"Video {request_body.video_id} not found", 404)

    if video.total_inventory <= 0:
        return make_response(f"Video is not availiable", 400)

    customer.videos_checked_out_count += 1
    video.total_inventory -= 1

    new_rental = Rental(
        customer_id=request_body["customer_id"],
        video_id=request_body["video_id"],
        due_date=date.today()+timedelta(days=7)
    )

    db.session.add(new_rental)
    db.session.commit()

    # return new_customer.get_json(), 201
    return {
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.total_inventory
    },200
