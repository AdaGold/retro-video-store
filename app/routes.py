from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
from app import db
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@customers_bp.route("", methods=["GET"])
def get_customers():
    '''
    Gets list of all customers
    '''
    customers = Customer.query.all()

    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_json())
    return jsonify(customers_response)

@customers_bp.route("", methods=["POST"])
def post_customer():
    '''
    Posts new customer
    '''
    request_body = request.get_json()

    if "name" not in request_body or "postal_code" not in request_body\
        or "phone" not in request_body:
        return ({
            "errors": ["Must input required data"]
        }, 400)
    else:
        new_customer = Customer.from_json(Customer, request_body)

        db.session.add(new_customer)
        db.session.commit()

        return {
            "id": new_customer.customer_id
        }, 201

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    '''
    Gets customer by customer_id
    '''
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("No customer found", 404)

    return {
        customer.to_json()
    }

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    '''
    Updates specific customer information
    '''
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("No customer found", 404)

    form_data = request.get_json()

    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = form_data["phone"]
    customer.registered_at = form_data["registered_at"]

    db.session.commit()

    return {
        "customer": customer.to_json()
    }

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    '''
    Deletes customer by customer_id
    '''
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("No customer found", 404)

    db.session.delete(customer)
    db.session.commit()

    return {
        "id": customer.customer_id
    }
