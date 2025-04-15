from flask import Blueprint, request
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from .route_utilities import validate_model, create_model
from datetime import datetime, timedelta
from ..db import db

bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")


@bp.post("/check-out")
def create_rental():
    request_body = request.get_json()

    customer_id = request_body.get("customer_id", "")
    customer = validate_model(Customer, customer_id)
    video_id = request_body.get("video_id", "")
    rented_video = validate_model(Video, video_id)

    for rental in customer.rentals:
        if rental.video_id == video_id and rental.status == "RENTED":
            message = f"Video {video_id} already rented by customer {customer_id}"
            return {"message": message}, 400

    if rented_video.get_available_inventory() == 0:
        response = {"message": "Could not perform checkout"}
        return response, 400

    due_date = datetime.now() + timedelta(days=7)
    request_body["due_date"] = due_date.strftime("%Y-%m-%d %H:%M:%S")

    return create_model(Rental, request_body, response_code=200)

@bp.post("/check-in")
def return_rental():
    request_body = request.get_json()

    customer_id = request_body.get("customer_id", "")
    customer = validate_model(Customer, customer_id)
    video_id = request_body.get("video_id", "")
    rented_video = validate_model(Video, video_id)

    to_return = None
    for rental in customer.rentals:
        if rental.video_id == video_id and rental.status == "RENTED":
            to_return = rental
            break

    if not to_return:
        message = f"No outstanding rentals for customer {customer_id} and video {video_id}"
        return {"message": message}, 400

    rental.status = "AVAILABLE"
    db.session.commit()
    return rental.to_dict()
