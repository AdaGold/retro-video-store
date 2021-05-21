from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import Blueprint, request, make_response
from app import db

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return None

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def check_out_video():
    check_out_data = request.get_json()
    if not is_int(check_out_data["customer_id"]) or not is_int(check_out_data["video_id"]):
        return make_response({"details": "Invalid ID"}, 400)

    customer = Customer.query.get_or_404(check_out_data["customer_id"])
    video = Video.query.get_or_404(check_out_data["video_id"])
    check_out_rental = Rental(**check_out_data)
    if video.available_inventory > 0:
        video.available_inventory -= 1
        customer.videos_checked_out_count += 1
        db.session.add(check_out_rental)
        db.session.commit()
        return make_response(check_out_rental.rental_to_json(), 200)
    return make_response({"details": "Inventory not available"}, 400)

@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def check_in_video():
    check_in_data = request.get_json()
    if not is_int(check_in_data["customer_id"]) or not is_int(check_in_data["video_id"]):
        return make_response({"details": "Invalid ID"}, 400)

    check_in_rental = Rental.query.get_or_404((check_in_data["customer_id"], check_in_data["video_id"]))
    if check_in_rental.customer.videos_checked_out_count > 0:
        check_in_rental.video.available_inventory += 1
        check_in_rental.customer.videos_checked_out_count -= 1
        db.session.commit()
        response_body = check_in_rental.rental_to_json()
        del response_body["due_date"]
        return make_response(response_body, 200)
    return make_response({"details": "Rentals all returned"}, 400)

