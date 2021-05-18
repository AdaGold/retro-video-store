from flask import Blueprint
from flask import request, Blueprint, make_response, jsonify, abort
from app.models.customer import Customer
from app import db

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")



@customers_bp.route("", methods=['GET', 'POST'])
def handle_customers():

    if request.method == 'GET':
        pass
    
    
    if request.method == 'POST':
        request_body = request.get_json()

        if "name" not in request_body or \
            "postal_code" not in request_body or \
            "phone" not in request_body:
                return ("", 400)
        
        else:
            new_customer = Customer(name = request_body["name"],
                                    postal_code = request_body["postal_code"],
                                    phone = request_body["phone"])
            
            db.session.add(new_customer)
            db.session.commit()

            return {"id": new_customer.id}, 201

        



@customers_bp.route("/<id>", methods=['GET', 'PUT', 'DELETE'])
def handle_customer_by_id():
    if request.method == 'GET':
        pass
        

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass
