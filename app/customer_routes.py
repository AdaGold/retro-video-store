from flask import request, Blueprint, make_response, jsonify
from app import db
from dotenv import load_dotenv
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from datetime import datetime


load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods = ["GET"])
def get_customers():
    #gets customers
    customers_query = Customer.query.all()

    return make_response(jsonify([customer.build_dict() for customer in customers_query]), 200)
@customers_bp.route("/<id>", methods = ["GET"])
def get_customer(id):
    #gets one customer
    customer = Customer.query.get_or_404(id)

    return make_response(customer.build_dict(), 200)

@customers_bp.route("", methods = ["POST"])
def add_customers():
    #adds customers
    request_body = request.get_json()
    if "name" not in request_body.keys() or "postal_code" not in request_body.keys() or "phone" not in request_body.keys():
        return make_response({"details" : "Insufficient data"}, 400) 
    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
        registered_at = datetime.now()
    )
    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.build_dict(), 201)

@customers_bp.route("/<id>", methods = ["PUT"])
def update_customers(id):
    #updates a customer
    customer = Customer.query.get_or_404(id)
    form_data = request.get_json()
    if "name" not in form_data.keys() or "postal_code" not in form_data.keys() or "phone" not in form_data.keys():
        return make_response({"details" : "Insufficient data"}, 400) 
    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = form_data["phone"]

    db.session.commit()

    return make_response(customer.build_dict(), 200)

@customers_bp.route("/<id>", methods = ["DELETE"])
def delete_customer(id):
    #deletes a customer
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()

    return make_response({"id" : customer.id}, 200)

@customers_bp.route("/<id>/rentals", methods = ["GET"])
def list_rentals(id):
    #lists all rentals for customer
    customer = Customer.query.get_or_404(id)
    rentals = customer.videos_checked_out
    results = [video.rentals_by_cust() for video in rentals]
    return make_response(jsonify(results), 200)

