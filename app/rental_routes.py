from flask import request, Blueprint, make_response, jsonify
from app import db
from dotenv import load_dotenv
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental

load_dotenv()

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods = ["POST"])
def check_out_rental():
    form_data = request.get_json()
    customer = Customer.query.get_or_404(form_data["customer_id"])
    video = Video.query.get_or_404(form_data["video_id"])
    rental = Rental(
        customer_id = form_data["customer_id"],
        video_id = form_data["video_id"]
    )
    rental = rental.build_dict()
    rental["available_inventory"] = video.available_inventory
    return make_response(rental, 200)

@rentals_bp.route("/check-in", methods = ["POST"])
def check_in_rental():
    form_data = request.get_json()
    customer = Customer.query.get_or_404(customer_id)
    video = Video.query.get_or_404(video_id)
    rental = Rental(
        customer_id = form_data["customer_id"],
        video_id = form_data["video_id"]
    )
    

    


