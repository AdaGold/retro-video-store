from app.models.customer import Customer
from app.models.video import Video

from app import db
from flask import json, request, Blueprint, make_response, jsonify
import os
import requests

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

'''
To Do:
PUT /customers/<id>
DELETE /customers/<id>
'''
@customers_bp.route("", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    customers_list = []
    for customer in customers:
        customers_list.append(customer.get_response())

    return jsonify(customers_list), 200

@customers_bp.route("/<id>", methods=["GET"])
def get_customer_id(id):
    customer = Customer.query.get(id)

    if customer == None: 
        return {"error":f"Customer ID {id} not found."}, 404
    return jsonify(customer.get_response()),200


@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return {"details":"Invalid data"}, 400
    new_customer = Customer(
                        name=request_body["name"],
                        postal_code=request_body["postal_code"],
                        phone=request_body["phone"])
    db.session.add(new_customer)
    db.session.commit()
    return {"id":new_customer.id},201

@customers_bp.route("/<id>", methods=["PUT"])
def update_customer_info(id):
    customer = Customer.query.get(id)
    form_data = request.get_json()

