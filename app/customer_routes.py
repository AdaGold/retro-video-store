from flask import Blueprint
from flask import request, Blueprint, make_response, jsonify, abort
from app.models.customer import Customer
from app import db

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")



@customers_bp.route("", methods=['GET', 'POST'])
def handle_customers():

    if request.method == 'GET':

        customer = Customer.query.all()
        
        customers = []

        for customer in customers:
            customers.append(customer.to_json())
        
        db.session.commit()
        return jsonify(customers), 200
    
    
    if request.method == 'POST':
        #customer = Query.args.get('id')
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
def handle_customer_by_id(id):

    customer = Customer.query.get(id)


    if customer == None:
            return ("", 404)

    else:
    
        if request.method == 'GET':
            return jsonify(customer.json_response()), 200


        elif request.method == 'PUT':
            update = request.get_json() 

            customer.name = update["name"]
            customer.postal_code = update["postal_code"]
            customer.phone = update["phone"]

            db.session.commit()
            return jsonify(customer.json_response()), 200
                

            

        elif request.method == 'DELETE':
            db.session.delete(customer)
            db.session.commit()
            return {"id": customer.id}
            
