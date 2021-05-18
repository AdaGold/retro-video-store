from app import db
from flask import Blueprint, request, jsonify
from app.models.customer import Customer
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():
    body = request.get_json() 

    if ("name" not in body.keys() or
        "postal_code" not in body.keys() or
        "phone_number" not in body.keys() or
        "register_at" not in body.keys()):
        return {"error" : "Invalid data"}, 400

    new_customer = Customer(name = body["name"],
                            postal_code = body["postal_code"],
                            phone_number = body["phone_number"])
    db.session.add(new_customer)
    db.session.commit()

    