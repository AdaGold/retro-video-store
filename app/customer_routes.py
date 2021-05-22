from flask import Blueprint, request, jsonify, make_response
from app import db 
from app.models.customer import Customer 
from datetime import date
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

        for customer in customers:
            customers_response.append(customer.get_json())
        return jsonify(customers_response), 200
            
# POST /customers
    elif request.method == "POST":  # CRUD CREATE
        
        request_body = request.get_json()
        
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return {
                "details": f"Not found"
            }, 400
 
        new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
            register_at=date.today(),
            videos_checked_out_count= 0
        )

        db.session.add(new_customer)
        db.session.commit()

        # return new_customer.get_json(), 201
        return {"id":new_customer.customer_id},201

# GET /customers/<id>
@customer_bp.route("/<customer_id>", methods=["GET","PUT","DELETE"])
def single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return make_response(f"Customer {customer_id} not found", 404) 

    if request.method == "GET":
        return customer.get_json(),200 

# PUT /customers/<id>
    elif request.method == "PUT":
        request_body = request.get_json()

        customer = Customer.query.get(customer_id)
        if customer == None:
            return make_response(f"Customer {customer_id} not found", 404)

        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return {
                "details": f"Not found"
            }, 400

        #update customer info
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone= request_body["phone"]
        
        db.session.commit()

        return customer.get_json(), 200  
        
# DELETE /customers/<id>
    elif request.method == "DELETE":
        
        customer = Customer.query.get(customer_id)
        if customer == None:
            return make_response(f"Customer {customer_id} not found", 404)
        
        db.session.delete(customer)
        db.session.commit()

        return {
            "id":int(customer_id)
        }, 200
        

        
