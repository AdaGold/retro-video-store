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
    #checks out one rental, creating an instance of Rental
    form_data = request.get_json()
    if rental_invalid(form_data):
        return make_response({"Details": "Invalid data"}, 400)
    video = Video.query.get(form_data["video_id"])
    customer = Customer.query.get(form_data["customer_id"])
    if video.calculate_inventory() <= 0:
        return make_response({"Details": "Invalid data"}, 400)

    rental = Rental(customer_id=customer.id,video_id=video.id)
    
    db.session.add(rental)
    db.session.commit()
    return make_response(rental.check_out_dict(),200)

@rentals_bp.route("/check-in", methods = ["POST"])
def check_in_rental():
    #checks in a rental, deleting the instance of Rental
    form_data = request.get_json()
    rentals = Rental.query.all()
    for rental in rentals:
        if rental.customer_id == form_data["customer_id"] and rental.video_id == form_data["video_id"]:
            rentals = rental

            db.session.delete(rentals)
            rental_dict = rentals.check_in_dict()
            db.session.commit()
            return make_response(rental_dict, 200)
    return make_response({"details": "this is already checked in"}, 400)


def rental_invalid(request):
    if "customer_id" not in request or "video_id" not in request:
        return True
    elif type(request["customer_id"]) != int or type(request["video_id"]) != int:
        return True
    else:
        return False

    


