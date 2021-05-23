from flask import Blueprint, request, make_response, jsonify
from app import db 
from app.models.customer import Customer
from app.models.video import Video 
from app.models.rental import Rental
from dotenv import load_dotenv
from datetime import datetime

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
load_dotenv()

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():

    customers = Customer.query.all()
    customers_respone = []

    if customers is None:
        return 404

    for customer in customers:
        customers_respone.append(customer.to_json_customer())

    return jsonify(customers_respone), 200


@customers_bp.route("", methods=["POST"], strict_slashes=False)
def new_customer():

    request_body = request.get_json()

    if "name" not in request_body.keys() or "postal_code" not in request_body.keys() or "phone" not in request_body.keys():

        error_response = {"errors": "enter info for all fields"}

        return jsonify(error_response), 400

    new_customer = Customer(name = request_body["name"], postal_code = request_body["postal_code"], phone_number = request_body["phone"])
    new_customer.registered_at = datetime.utcnow()
    db.session.add(new_customer)
    db.session.commit()

    valid_customer = new_customer.to_json_customer()

    return jsonify(valid_customer), 201

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def handle_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if request.method == "GET":
        if customer is None:
            return make_response(f"404 Not Found", 404) 

        else:
            one_customer = customer.to_json_customer()

            return jsonify(one_customer)

@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer:
        db.session.delete(customer)
        db.session.commit()

        return {"id": customer.id}, 200
    
    else:
        return make_response(f"Customer {customer_id} does not exist", 404)

@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):

    customer = Customer.query.get(customer_id)
    form_data = request.get_json()

    if customer:
    
        if "name" in form_data.keys() or "phone" in form_data.keys() or "postal_code" in form_data.keys():
            
            customer.name = form_data["name"]
            customer.phone_number = form_data["phone"]
            customer.postal_code = form_data["postal_code"]
            
            db.session.commit()
        
            updated_customer = customer.to_json_customer()

            return jsonify(updated_customer), 200
        
        else:
            return jsonify({"error": f"Customer {customer_id} not relevant"}), 400
    
    else:
        return make_response("Customer does not exist", 404)
        

@customers_bp.route("/<id>/rentals", methods=["GET"], strict_slashes=False)
def customer_videos(id):

    # create instance of customer using customer id 
    request_body = request.get_json()
    customer = Customer.query.get(id)
    videos_list = []

    # if customer exists
    if customer:

        # create join table 
        results = db.session.query(Customer, Video, Rental)\
            .join(Customer, Customer.id==Rental.customer_id)\
                .join(Video, Video.id==Rental.video_id)\
                    .filter(Customer.id==customer.id).all()

        unpack_join = results[0]
        print(unpack_join)

        customer = unpack_join[0]
        print(customer)
        video = unpack_join[1]
        print(video)

        rental = unpack_join[2]

        response = {
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.due_date
        }

        print(request_body["video_id"])

        return make_response(f"{rental.id}", 200)

    else:
        if customer is None:
            return {"Error": "Customer does not exist"}, 404


