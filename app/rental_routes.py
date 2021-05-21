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
    if rental_invalid(form_data):
        return make_response({"Details": "Invalid data"}, 400)
    video = Video.query.get(form_data["video_id"])
    customer = Customer.query.get(form_data["customer_id"])
    rental = Rental(customer_id=form_data["customer_id"],video_id=form_data["video_id"])
    video.customers_rented_to = customer.id
    video.calculate_inventory()

    db.session.add(rental)
    db.session.commit()
    return make_response(rental.build_dict(),200)

# @rentals_bp.route("/check-in", methods = ["POST"])
# def check_in_rental():
#     form_data = request.get_json()
#     rental = Rental.query.get_or_404(form_data["customer_id"], form_data["video_id"])
    
#     db.session.delete(rental)
#     rental_dict = rental.build_dict()
#     db.session.commit()
#     return make_response(rental_dict, 200)


def rental_invalid(request):
    if "customer_id" not in request or "video_id" not in request:
        return True
    if type(request["customer_id"]) != int or type(request["video_id"]) != int:
        return True
    if Video.query.get_or_404(request["video_id"]).available_inventory == 0:
        return True
    else:
        return False

    


