from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import jsonify
from flask import request, make_response
import os


customers_bp = Blueprint("customer", __name__, url_prefix="/customer")
videos_bp = Blueprint("video", __name__, url_prefix="/video")
#rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals") ### might not need this one



@customers_bp.route("", methods=["POST"])
def handle_customers():
    request_body = request.get_json()
    new_customer = Customer(name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
            registered_at=request_body["registered_at"])
    db.session.add(new_customer)
    db.commit()
    return make_response({"customer":new_customer.to_json()}, 201)

@customers_bp.route("", methods=["GET"])
def get_customers_details():
    pass

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    pass

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    pass

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    pass

