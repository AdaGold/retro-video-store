from flask import request, Blueprint, make_response, jsonify
from app import db
from dotenv import load_dotenv
from app.models.customer import Customer
from datetime import datetime

load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods = ["GET"])
def get_customers():
    '''gets all customers from database'''
    customers_query = Customer.query.all()

    return make_response(jsonify([customer.build_dict() for customer in customers_query]))
@customers_bp.route("/<id>", methods = ["GET"])
def get_customer(id):
    '''gets one customer'''
    customer = Customer.query.get_or_404(id)

    return make_response({"customer": customer.build_dict()}, 200)

@customers_bp.route("", methods = ["POST"])
def add_customers():
    '''adds customers'''
    request_body = request.get_json()
    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
        register_at = datetime.now()
    )
    db.session.add(new_customer)
    db.session.commit()

    return make_response(new_customer.build_dict(), 201)

@customers_bp.route("/<id>", methods = ["PUT"])
def update_customers(id):
    '''updates a customer '''
    customer = Customer.query.get_or_404(id)
    form_data = request.get_json()
    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = request_body["phone"]
    customer.register_at = datetime.now()

    db.session.commit()

    return make_response({"customer": customer.build_dict()}, 200)

@customers_bp.route("/<id>", methods = ["DELETE"])
def delete_customer(id):

    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()

    return make_response({"details" : f"Customer {customer.name} has been deleted"})