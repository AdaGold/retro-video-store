from flask import request, Blueprint, make_response, jsonify
from app import db
from dotenv import load_dotenv
from app.models.customer import Customer
from app.models.video import Video

load_dotenv()

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods = ["POST"])
def check_out_rental(customer_id, video_id):
    customer = Customer.query.get_or_404(customer_id)
    video = Video.query.get_or_404(video_id)
    customer.videos_checked_out_count.append(video)
    return make_response(customer.rent_video(video), 200)

@rentals_bp.route("/check-in", methods = ["POST"])
def check_in_rental(customer_id, video_id):
    customer = Customer.query.get_or_404(customer_id)
    video = Video.query.get_or_404(video_id)
    customer.videos_checked_out_count.remove(video)
    return make_response(video.return_video(video), 200)

    


