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
    return jsonify(response), 200


@customers_bp.route("", methods=["POST"])
def add_customer():
    """Creates a new video with the given Request Body Parameters."""
    request_body = request.get_json()

    if not (
            "name" in request_body and "postal_code" in request_body and "phone" in request_body):
        return make_response({
            "errors": [
                "Bad Request",
                "'name' is required",
                "'postal_code' is required",
                "'phone' is required"
            ]
        }, 400)

    new_customer = Customer()
    new_customer = new_customer.from_json(request_body)
    db.session.add(new_customer)
    db.session.commit()

    # retrieve_customer = Customer.query.get(new_customer.customer_id)
    return make_response(new_customer.to_json(), 201)


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    """Gives back details about specific customer."""
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response({
            "errors": [
                "Not Found",
                "Customer does not exist"
            ]
        }, 400)
    return make_response(customer.to_json(), 200)


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer_by_id(customer_id):
    """Updates and returns details about specific customer."""
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response({
            "errors": [
                "Not Found",
                "Customer to update does not exist"
            ]
        }, 400)

    request_body = request.get_json()

    if not (
            "name" in request_body and "postal_code" in request_body and "phone" in request_body):
        return make_response({
            "errors": [
                "Bad Request",
                "'name' is required",
                "'postal_code' is required",
                "'phone' is required"
            ]
        }, 400)

    customer = customer.from_json(request_body)
    db.session.commit()
    retrieve_customer = Customer.query.get(customer_id)

    return make_response(retrieve_customer.to_json(), 200)


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id):
    """Deletes a specific customer."""
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response({
            "errors": [
                "Not Found",
                "Customer to delete does not exist"
            ]
        }, 404)

    db.session.delete(customer)
    db.session.commit()
    # return ({"id": customer_id, "details": 'Task has been successfully
    # deleted'}, 200)
    return ({"id": customer_id}, 200)

# -------------- CRUD for /videos ------------------------

