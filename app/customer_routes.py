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
        "phone" not in body.keys()):
        return {"error" : "Invalid data"}, 400

    new_customer = Customer(name = body["name"],
                            postal_code = body["postal_code"],
                            phone = body["phone"],
                            register_at = datetime.utcnow())
    db.session.add(new_customer)
    db.session.commit()

    return {
        "id": new_customer.customer_id
    },201


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    name_from_url = request.args.get("name")

    if name_from_url:
        customers = Customer.query.filter_by(name = name_from_url)
    
    customers = Customer.query.all()

    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_json())

    return jsonify(customer_response), 200


def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False


@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer_by_id(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return ("", 404)
    
    if not is_int(customer_id):
        return ("", 400)
    
    return customer.to_json(), 200 


@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return ("", 404)
    
    if not is_int(customer_id):
        return ("", 400)
    
    form_data = request.get_json()

    if ("name" not in  form_data.keys() or
        "postal_code" not in form_data.keys() or
        "phone" not in form_data.keys()):
        return {"error" : "Invalid data"}, 400

    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = form_data["phone"]

    db.session.commit()

    return customer.to_json(), 200


@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer is None:
        return ("", 404)
    
    if not is_int(customer_id):
        return ("", 400)
    
    db.session.delete(customer)
    db.session.commit()

    return {"id": customer.customer_id},200