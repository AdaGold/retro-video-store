from app import db
from flask import Blueprint, request, make_response, jsonify
from .models.customer import Customer
from .models.video import Video



customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


def error_handling(request_body):
    if "name" or "postal_code" or "phone" not in request_body:
        return True
    
    # if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
    #     return make_response({"details": "Invalid data"}, 400)
    

@customers_bp.route("", methods=["POST"])
def create_customer():
    
    request_body = request.get_json()
    customer = Customer(customer_name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone_number=request_body["phone"],
                    )

    db.session.add(customer)
    db.session.commit()

    return make_response(customer.return_customer_info(), 201)

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customer_list = []
    for customer in customers:
        customer_list.append(customer.return_customer_info())

    return jsonify(customer_list), 200

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    form_data = request.get_json()
    #handle 404 function

    return make_response(customer.return_customer_info(), 200)

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer_info(customer_id):
    #can I make helper function for .query.get and form_data?
    if not customer_id:
        return 404
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
    customer = Customer.query.get(customer_id)
    form_data = request.get_json()

    customer.customer_name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone_number = form_data["phone"]

    db.session.commit()

    return make_response(customer.return_customer_info())

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    Customer.query.filter_by(customer_id=customer_id).delete()
    # db.session.delete(customer) 
    db.session.commit()

    return make_response({"id":customer_id}, 200)

