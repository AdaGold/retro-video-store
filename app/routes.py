from flask import Blueprint, make_response, jsonify, request
from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

# -------------- CRUD for /customers ------------------------


@customers_bp.route("", methods=["GET"])
def get_all_customers():
    """Lists all existing customers and details about each customer."""
    customers = Customer.query.all()
    response = [customer.to_json() for customer in customers]
    return jsonify(response)


@customers_bp.route("", methods=["POST"])
def add_customer():
    """Creates a new video with the given Request Body Parameters."""
    request_body = request.get_json()

    if not (
            "name" in request_body and "postal_code" in request_body and "phone" in request_body):
        return make_response({
            "errors": [
                "Invalid input data"
            ]
        }, 400)

    new_customer = Customer()
    new_customer = new_customer.from_json(request_body)
    db.session.add(new_customer)
    db.session.commit()

    # retrieve_customer = Customer.query.get(new_customer.customer_id)
    return make_response({"id": new_customer.customer_id}, 201)
