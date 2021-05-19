from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
from app import db
from datetime import datetime



customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")


@customer_bp.route("", methods=["POST"])
def valid_customer():

    form_data = request.get_json()
    if "name" not in form_data\
        or "postal_code" not in form_data\
            or "phone" not in form_data:
        return make_response({"details":"Invalid data"}, 400)
    else:
        new_customer = Customer(name=form_data["name"],
                                postal_code=form_data["postal_code"],
                                phone=form_data["phone"])

    if new_customer:
        new_customer.registered_at = datetime.utcnow()
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.customer_id}), 201


@customer_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = []
    for customer in customers:
        customers_response.append(customer.cust_dict())
    return jsonify(customers_response)


@customer_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return (customer.cust_dict())


@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    '''update single customer'''
    customer = Customer.query.get_or_404(customer_id) 

    form_data = request.get_json()
    if "name" not in form_data\
        or "postal_code" not in form_data\
            or "phone" not in form_data:
        return make_response({"details":"Invalid data"}, 400)
    
    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = form_data["phone"]
    db.session.commit()
    return jsonify(customer.cust_dict()), 200

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer= Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return {"id": customer.customer_id}



