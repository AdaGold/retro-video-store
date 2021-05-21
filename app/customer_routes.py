from flask import Blueprint
from flask import request, Blueprint, make_response, jsonify, abort
from app.models.customer import Customer
from app import db



customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=['GET', 'POST'])
def handle_customers():
    customers = Customer.query.all()
    request_body = request.get_json()

    if customers == None:
        return("", 404)

    if request.method == 'GET':
        customers_list = [customer.json_response() for customer in customers]
        return jsonify(customers_list)
    
    
    elif request.method == 'POST':

        if "name" not in request_body or \
            "postal_code" not in request_body or \
            "phone" not in request_body:
                return {"error" : "Invalid data"}, 400
        
        else:
            new_customer = Customer(name = request_body["name"],
                                    postal_code = request_body["postal_code"],
                                    phone = request_body["phone"])
            
            db.session.add(new_customer)
            db.session.commit()

            return {"id": new_customer.id}, 201

        


@customers_bp.route("/<id>", methods=['GET', 'PUT', 'DELETE'])

def handle_customer_by_id(id):
    CUSTOMER_ID = Customer.query.get(id)
    REQUEST_BODY = request.get_json()


    if CUSTOMER_ID == None:
        return ("", 404)

    else:
    
        if request.method == 'GET':
            return jsonify(CUSTOMER_ID.json_response()), 200


        elif request.method == 'PUT':

            if "name" not in REQUEST_BODY or \
            "postal_code" not in REQUEST_BODY or \
            "phone" not in REQUEST_BODY:
                return {"error" : "Invalid data"}, 400
    

            CUSTOMER_ID.name = REQUEST_BODY["name"]
            CUSTOMER_ID.postal_code = REQUEST_BODY["postal_code"]
            CUSTOMER_ID.phone = REQUEST_BODY["phone"]

            db.session.add(CUSTOMER_ID)
            db.session.commit()
            return jsonify(CUSTOMER_ID.json_response()), 200
                

            

        elif request.method == 'DELETE':
            db.session.delete(CUSTOMER_ID)
            db.session.commit()
            return {"id": CUSTOMER_ID.id}
            
