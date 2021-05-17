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

    return make_response([customer.id for customer in customers_query])
@customers_bp.route("/<customer_id>", methods = ["GET"])
def get_customer(customer_id):
    '''gets one customer'''
    customer = Customer.query.get_or_404(customer_id)

    return make_response({"customer": customer.build_dict()}, 200)

@customers_bp.route("", methods = ["POST"])
def add_customers():
    '''adds customers'''
    request_body = request.get_json()
    new_customer = Customer(
        name = request_body["name"],
        phone = request_body["phone"],
        register_at = datetime.now()
    )
    db.session.add(new_customer)
    db.session.commit()

    return make_response({"customer" : new_customer.build_dict()}, 200)

@customers_bp.route("/<customer_id", methods = ["PUT"])
def update_customers(customer_id):
    '''updates a customer '''
    customer = Customer.query.get_or_404(customer_id)
    form_data = request.get_json()
    customer.name = form_data["name"],
    phone = request_body["phone"],
    register_at = request_body["register_at"]

    db.session.commit()

    return make_response({"customer": customer.build_dict()}, 200)

@customers_bp.route("/<customer_id", methods = ["DELETE"])
def delete_customer(customer_id):

    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()

    return make_response({"details" : f"Customer {customer.name} has been deleted"})