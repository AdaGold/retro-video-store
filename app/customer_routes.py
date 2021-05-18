from app import db, helper
from .models.customer import Customer
#from .models.video import Video
from flask import request, Blueprint, make_response, jsonify, Response
from sqlalchemy import desc, asc
from datetime import date
import os
import requests
import json

#WAVE 1 CRUD /CUSTOMERS

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")

# GET all customers
@customer_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    
    customers = Customer.query.all()
    
    customer_response =[]
    for customer in customers:
        customer_response.append(customer.details_of_customer_response())
    return jsonify(customer_response), 200


#GET customers with specific ID
@customer_bp.route("/<id>", methods=["GET"], strict_slashes=False)
def get_specific_customers(id):
    
    if not helper.is_int(id):
        return {
            "message": "id must be an integer",
            "success": False
        },400
    
    customer =  Customer.query.get(id)
    
    if customer == None:
        return Response ("" , status=404)
    
    if customer:
        return make_response(customer.details_of_customer_response(), 200)
    

#POST /customers details
@customer_bp.route("", methods=["POST"], strict_slashes=False)
def add_customers():
    
    request_body = request.get_json()
    
    if ("name" not in request_body or 
        "postal_code" not in request_body or 
        "phone" not in request_body):
        
        return jsonify(details="Invalid data"),400
    
    new_customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"])
    
    db.session.add(new_customer)
    db.session.commit()
    
    return jsonify(id=new_customer.customer_id) ,201


#PUT update a customer detail
@customer_bp.route("<id>", methods=["PUT"], strict_slashes=False)
def update_customer(id):
    
    customer = Customer.query.get(id)
    
    if customer == None or not customer:
        return Response("", status=404)
    
    
    form_data = request.get_json()
    
       # validate request body 
    if not form_data or not form_data["name"] or not form_data["postal_code"] or not form_data["phone"]:
        return Response("", 400)
        
    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = form_data["phone"]
    
    db.session.commit()
    
    return customer.details_of_customer_response(), 200
    

#DELETE a customer
@customer_bp.route("/<id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(id):
    
    customer = Customer.query.get(id)
    
    if customer == None:
        return Response("", status=404)
    
    if customer:
        db.session.delete(customer)
        db.session.commit()
        
        return jsonify(id=id),200
    

        
    

        
