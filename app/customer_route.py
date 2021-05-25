from app import db
from app.models.customer import Customer
from app.models.video import Video
from flask import request, Blueprint, make_response,jsonify
from datetime import datetime 
import requests
import json



customer_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customer_bp.route("", methods=["GET", "POST"])
def handle_customer_get_post_all():
    if request.method == "GET":
        
        
        customer_list = Customer.query.all()

            
        customer_response = []

        for customer in customer_list:
        
            customer_response.append(customer.json_object())
        
        return jsonify(customer_response), 200

    elif request.method == "POST":

        request_body = request.get_json()

        if ("name" not in request_body) or ("postal_code" not in request_body) or ("phone" not in request_body):
            return make_response({
                "details": "Invalid data"
            }), 400
    
        new_customer = Customer(name=request_body["name"],
                        postal_code=request_body["postal_code"],
                        phone=request_body["phone"])

        if new_customer.registered_at == None:
            new_customer.registered_at = datetime.now()

        db.session.add(new_customer)
        db.session.commit()

        return make_response({"id": new_customer.customer_id}), 201


@customer_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_single_customer(customer_id):
    customer = Customer.query.get(customer_id) #fetching the customer OBJECT using the customer ID
    #when I request in the url and have no details return None and a 404 message
    if customer is None: #If customer 
        return jsonify(None), 404

    if request.method == "GET":

        return make_response(customer.json_object(), 200)

    elif request.method == "PUT":
        request_body = request.get_json()
        
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)
        form_data = request.get_json()

        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"] 

        db.session.commit()

        return make_response(customer.json_object())

    elif request.method == "DELETE":

        db.session.delete(customer)
        db.session.commit()
        return make_response({"id": customer.customer_id}, 200)