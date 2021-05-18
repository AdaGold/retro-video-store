from flask import Blueprint, request, make_response, jsonify
from app import db 
from app.models.customer import Customer
from dotenv import load_dotenv
import os 

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
load_dotenv()


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():

    customers = Customer.query.all()
    customers_respone = []

    if customers is None:
        return 404

    for customer in customers:
        customers_respone.append(customer.to_json_customer())

    return jsonify(customers_respone), 200


@customers_bp.route("", methods=["POST"], strict_slashes=False)
def new_customer():

    request_body = request.get_json()

    if "name" not in request_body.keys() or "postal_code" not in request_body.keys() or "phone" not in request_body.keys():
        
        error_response = {"errors": "enter info for all fields"}

        return jsonify(error_response), 400

    new_customer = Customer(name = request_body["name"], postal_code = request_body["postal_code"], phone_number = request_body["phone"])
    db.session.add(new_customer)
    db.session.commit()

    valid_customer = new_customer.to_json_customer()

    return jsonify(valid_customer), 201

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def handle_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if request.method == "GET":
        if customer is None:
            return make_response(f"404 Not Found", 404) 

        else:
            one_customer = customer.to_json_customer()

            return jsonify(one_customer)
