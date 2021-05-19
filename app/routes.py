from flask import request, Blueprint, Response, jsonify, make_response
from app import db
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime

# route for customers
customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
# route for videos
videos_bp = Blueprint("videos",__name__, url_prefix="/videos")


@customer_bp.route("", methods=["GET", "POST"])
def all_customers():
    if request.method == "GET":
        customers = Customer.query.all()
        customers_response = []
        for one_customer in customers:
            customers_response.append(one_customer.to_json())
        
        return jsonify(customers_response)
    
    elif request.method == "POST":
        request_body = request.get_json()
        # Create a customer: Invalid Task With Missing Data
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response ({"details": "Invalid data"}),400
        else:
            new_customer= Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"])
        db.session.add(new_customer)
        db.session.commit()

# they want us to return a the id only 
        return make_response({"id": new_customer.customer_id}), 201 


@customer_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"])
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    
    # GET/PUT/DELETE request to /customers/1 when there are no matching tasks and get this response
    #if customer == None:
    #    return make_response("",400)

    if request.method == "GET":
        if customer == None:
            return make_response("",404)
        else:
            return make_response({customer.to_json()}), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        if customer == None:
            return make_response("",404)
        elif "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response ({"details": "Invalid data"}),400    
        # converting postman json to a dict table
        else:
            form_data = request.get_json()

            customer.name = form_data["name"]
            customer.postal_code = form_data["postal_code"]
            customer.phone = form_data["phone"]

            db.session.commit()
            return make_response({customer.to_json()}), 200
    
    elif request.method == "DELETE":
        if customer == None:
            return make_response("",404)
# DELETE requests do not generally include a request body, so 
# no additional planning around the request body is needed        
        else:
            db.session.delete(customer)
            db.session.commit()
            return make_response ({"id": customer.customer_id}), 200

@videos_bp.route("", methods=["GET", "POST"])
def all_customers():
    if request.method == "GET":
        videos = Video.query.all()
        videos_response = []
        for one_video in videos:
            videos_response.append(one_video.to_json())
        
        return jsonify(videos_response)



#@videos_bp.route("/<video_id>", methods=["GET", "PUT","DELETE"])