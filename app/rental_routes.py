from flask import request, Blueprint, make_response, jsonify
from app import db
from dotenv import load_dotenv
from .customer import Customer
from .video import Video

load_dotenv()

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@rentals_bp.route("/check-out", methods = ["GET"])
def check_out_rental(customer_id, video_id):
    customer = Customer.query.get_or_404(customer_id)
    video = Video.query.get_or_404(video_id)
    customer.videos_checked_out_count.append(video_id)
    video.available_inventory -= 1
    return make_response(customer.rent_video(video_id))

