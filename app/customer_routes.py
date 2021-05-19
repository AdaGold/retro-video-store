from flask import Blueprint, request, jsonify, make_response
from app import db 
from app.models.customer import Customer 
from sqlalchemy import asc, desc
from datetime import datetime
import os, requests
from dotenv import load_dotenv

load_dotenv()   #???

customer_bp=Blueprint("customers",__name__, url_prefix="/customers")    

# GET /customers
@customer_bp.route("", methods=["GET","POST"])   #strict_slashes=False??
def list_customers():   #ok def name?
# GET /customers
    if request.method == "GET":

        customers = Customer.query.all()
        customers_response = []

        #can I call register_at() method?
        for customer in customers:
            if customer.register.at == None:
                register_at=False
            else:
            register_at = True

            customers_response.append({
                "id": customer.customer_id,
                "name": customer.name,
                "register_at": customer.description,
                "postal_code": customer.postal_code,
                "phone": customer.phone,
                "videos_checked_out": customer.videos_checked_out
            },
            {
                "id": customer.customer_id,
                "name": customer.name,
                "register_at": customer.description,
                "postal_code": customer.postal_code,
                "phone": customer.phone,
                "videos_checked_out": customer.videos_checked_out
            }
            ), 200
            #sort???

# POST /customers
    elif request.method == "POST":  # CRUD CREATE
        # check for request body title and description, plus ensure both are strings
        request_body = request.get_json()
        # 41 correct?
        if "name" not in request_body or "register_at" not in request_body or "postal_code" not in request_body or "phone" not in request_body or "videos_checked_out" not in request_body:
            return {
                "details": f"Not found"
            }, 404

        register_at = request_body["register_at"]

        customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"]
        )

        db.session.add(customer)
        db.session.commit()

        if is_register== None:
            register_at=False
        else:
            register_at = True
        return {
            "id":customer.customer_id
        }, 201

# GET /customers/<id>
@customer_bp.route("/<customer_id>", methods=["GET","PUT","DELETE"])
def single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return make_response(f"Customer {customer_id} not found", 404) 

    if request.method == "GET":
        if customer.register_at == None:
            register_at = False
        else:
            register_at=True
        return {"customer":customer.get_json()},200 #should I put customer_id instead?


# PUT /customers/<id>
    elif request.method == "PUT":
        form_data = request.get_json()
    
     #update customer = customer
        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone= form_data["phone"]

        db.session.commit()

        if customer.register_at == None:
            register_at = False
        else:
            register_at=True
        return {
            "customer": {
                "id": customer.customer_id,
                "name": customer.title,
                "register_at": customer.register_at,
                "phone": customer.phone,
                "videos_checked_out_count":customer.videos_checked_out_count
            }
        }, 404  #Right error?
        # need 400: Bad Request, if any of the request body fields are missing or invalid

# DELETE /customers/<id>
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        
        if customer.register_at == None:
            register_at = False
        else:
            register_at=True
        return {
            # "details": f"Customer {customer.customer_id} \"{customer.name}\" successfully deleted"
        }, 200
        # 404: Not Found if this customer does not exist???
