from flask import request, Blueprint, make_response, jsonify
from app import db
from dotenv import load_dotenv
from app.models.customer import Customer

load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods = ["GET"])
def get_customers():
    '''gets all customers from database'''
    customers_query = Customer.query.all()

    return make_response([customer.id for customer in customers_query])
@customers_bp.route("/<customer_id>", methods = ["GET"])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    return make_response(customer.build_dict(), 200)
