from flask import Blueprint, request
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from .route_utilities import validate_model, create_response_for_model, date_to_str
from ..db import db

bp = Blueprint("rentals_bp", __name__, url_prefix="/rentals")


@bp.post("/check-out")
def create_rental():
    request_body = request.get_json()

    customer_id = request_body.get("customer_id", "")
    customer = validate_model(Customer, customer_id)
    video_id = request_body.get("video_id", "")
    video_to_rent = validate_model(Video, video_id)

    if customer.has_active_rental(video_id):
        message = f"Video {video_id} already rented by customer {customer_id}"
        return {"message": message}, 400

    if not video_to_rent.is_available():
        response = {"message": "Could not perform checkout"}
        return response, 400

    request_body["due_date"] = date_to_str(Rental.calculate_due_date())
    return create_response_for_model(Rental, request_body, response_code=200)

@bp.post("/check-in")
def return_rental():
    request_body = request.get_json()

    customer_id = request_body.get("customer_id", "")
    customer = validate_model(Customer, customer_id)
    video_id = request_body.get("video_id", "")
    _ = validate_model(Video, video_id)

    try:
        rental = customer.get_active_rental_by_video_id(video_id)
    except ValueError:
        message = f"No outstanding rentals for customer {customer_id} and video {video_id}"
        return {"message": message}, 400

    rental.return_rental()
    db.session.commit()
    
    return rental.to_dict()
