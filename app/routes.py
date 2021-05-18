from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, jsonify
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

def get_customer_response(customer, code=200):
    return customer.to_dict(), code

def get_client_error_response(code=400):
    return {"details": "Invalid data"}, code


@customers_bp.route("", methods=["GET"])
def get_customers():
    """Lists all existing customers and details about each customer."""  
    customers = Customer.query.all()
    response_body = [] 
    for customer in customers:
        response_body.append(customer.to_dict())
    return jsonify(response_body), 200

@customers_bp.route("/<customer_id>", methods=["GET"]) 
def get_customer_info(customer_id):
    """Gives back details about specific customer."""
    customer = Customer.query.get(customer_id)
    if not customer:
        return get_client_error_response(code=404)
    return get_customer_response(customer) 

@customers_bp.route("", methods = ["POST"])
def add_customer():
    """Adds new customer."""
    request_body = request.get_json()
    if len(request_body) != 3:
        return get_client_error_response()
    customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"]
        )  
    db.session.add(customer)
    db.session.commit()
    return jsonify({"id": customer.customer_id}), 201

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """Updates and returns details about specific customer."""
    customer = Customer.query.get(customer_id)
    if not customer:
        return get_client_error_response(code=404)
    request_body = request.get_json()
    if len(request_body) != 3:
        return get_client_error_response()
    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]
    db.session.commit()
    return get_customer_response(customer)

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Deletes a specific customer."""
    customer = Customer.query.get(customer_id)
    if not customer:
        return get_client_error_response(code=404)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"id": int(customer_id)}), 200
