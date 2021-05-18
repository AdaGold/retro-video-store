from app import db
from flask import Blueprint, request, jsonify
from app.models.customer import Customer
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    body = request.get_json() 

    new_customer = Customer(name = body["name"],
                            postal_code = body["postal_code"],
                            phone_number = body["phone_number"])