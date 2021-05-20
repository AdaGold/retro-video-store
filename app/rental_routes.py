from app import db
from flask import Blueprint, request, jsonify
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video


rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out",methods=["POST"], strict_slashes=False)
def create_rental():
    body = request.get_json()

    if ("customer_id" not in body.keys() or
        "video_id" not in body.keys()):
        return {"error" : "Invalid data"}, 400
    
    new_rental = Rental(customer_id = body["customer_id"],
                        video_id = body["video_id"])

    db.session.add(new_rental)
    db.session.commit()

    customer = Customer.query.get(body["customer_id"])
    video = Video.query.get(body["video_id"])

    return {
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.get_checked_out(),
        "available_inventory": video.get_available_inventory()
    }, 200