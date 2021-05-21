from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import Blueprint, request, jsonify, make_response
from app import db 

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers = Customer.query.all() 
    customers_response = [] 

    for customer in customers: 
        customers_response.append(customer.to_json())

    return jsonify(customers_response), 200

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    
    if customer: 
        return jsonify(customer.to_json()), 200
    
    return make_response("", 404)

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def post_customer(): 
    request_body = request.get_json()
    
    keys = ["name", "postal_code", "phone"]
    for key in keys: 
        if key not in request_body:
            return {"details": "Invalid data"}, 400

    new_customer = Customer.make_a_customer(request_body, id=None)

    db.session.add(new_customer)
    db.session.commit() 
    return {"id": new_customer.customer_id},201

@customers_bp.route("<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    
    if customer: 
        update_data = request.get_json() 
        
        keys = ["name", "postal_code", "phone"]
        for key in keys: 
            if key not in update_data or bool(update_data) is False:
                return {"details": "Invalid data"}, 400

        customer.name = update_data["name"]
        customer.postal_code = update_data["postal_code"]
        customer.phone = update_data["phone"]

        db.session.commit()
        return jsonify(customer.to_json()), 200
    
    return make_response("", 404)

@customers_bp.route("<int:customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)

    if customer: 
        db.session.delete(customer)
        db.session.commit()
        
        return {
            "id": customer_id
        }, 200 
    
    return make_response("", 404)

@customers_bp.route("<int:customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_rentals_from_customers(customer_id): 
    customer = Customer.query.get(customer_id)

    if customer: 
        rentals = Rental.query.filter_by(customer_id=customer_id).all()
        rental_list = [] 

        if rentals != None: 
            for rental in rentals: 
                video = Video.query.get(rental.video_id)
                rental_list.append(rental.customers_associated_rentals(video))
            return jsonify(rental_list), 200
        return jsonify(rental_list), 200 
    
    return make_response("", 404)
