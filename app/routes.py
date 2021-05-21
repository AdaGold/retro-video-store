from app import db
from flask import request, Blueprint, jsonify
from .models import Customer, Video
import datetime
import requests
import os

# Create an endpoint specifically for customers (all the routes start with /customers):
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

# GET /customers (define a route with default empty string for GET)
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers_index():
    # this is a class object (or variable) called query with .all() function which will get us all the customers
    customers = Customer.query.all() 

    # build list that has all the customers in it:
    customers_response = []

    for customer in customers:
        customers_response.append(customer.to_dict())   # SAME AS:
        # customers_response.append({
        #     "id": customer.id,
        #     "name": customer.name,
        #     "postal_code": customer.postal_code,
        #     "phone_number": customer.phone_number,
        #     "registered_at": customer.registered_at
        # })
    return jsonify(customers_response), 200  ### DO I NEED TO JSONIFY A DICTIONARY???

# GET /customers/<id> (define a new route to GET a specific customer)
@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_one_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400
    
    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404
    else:
        customer_dict = customer.to_dict()
     
    return jsonify({"customer": customer_dict}), 200

# POST /customers (define a route with default empty string for POST)
@customers_bp.route("", methods=["POST"], strict_slashes=False)
# when it gets a POST request (from postman in our case), it calls this function:
def create_customer():  

    # this will look at the http request received and give us the JSON in the body as a Python dictionary
    request_body = request.get_json()

    if not request_body.get("name") or not request_body.get("postal_code") \
        or not request_body.get("phone_number") or not request_body.get("registered_at"):
        return jsonify({"details": "Invalid data"}), 400 
    
    ### EXTRA If name not unique, print error message

    # make new customer:
    new_customer = Customer(name = request_body["name"], \
        postal_code = request_body["postal_code"], \
            phone_number = request_body["phone_number"], \
                registered_at = request_body["registered_at"])

    db.session.add(new_customer)   # this tells SQLAlchemy to add this new_book/model to the db (like staging, can stage multiple items)
    db.session.commit()     # this tells SQLAlchemy to commit the stages and make it happen (doing the action)

    # we need an extra step to transfer completed_at to is_completed:
    customer_dict = new_customer.to_dict()

    return jsonify({"customer": customer_dict}), 201


# PUT /customers/<id> (define a new route to update (PUT) one customer by its id):
@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_single_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400
    
    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404

    form_data=request.get_json()

    if not form_data.get("name") or not form_data.get("postal_code") \
        or not form_data.get("phone_number"):
        return jsonify({"details": "Invalid data"}), 400 

    customer.name=form_data["name"]
    customer.postal_code=form_data["postal_code"]
    customer.phone_number=form_data["phone_number"]
    db.session.commit()

    # we need an extra step to transfer completed_at to is_completed:
    customer_dict = customer.to_dict()
    
    return jsonify({"customer": customer_dict}), 200

# DELETE /customers/<id> (define a new route to DELETE one task by its id):
@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404
   
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"details": f'Customer {customer.id} "{customer.name}" successfully deleted'}), 200


# Create an endpoint specifically for videos (all the routes start with /customers):
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


# GET /videos
@videos_bp.route("", methods=["GET"], strict_slashes=False)
def videos_index():
    # this is a class object (or variable) called query with .all() function which will get us all the customers
    videos = Video.query.all() 

    # build list that has all the customers in it:
    videos_response = []

    for video in videos:
        videos_response.append(video.to_dict())   # SAME AS:
        # videos_response.append({
        #     "id": video.id,
        #     "title": video.title,
        #     "release_date": video.release_date,
        #     "inventory": video.inventory
        # })
    return jsonify(videos_response), 200 

# GET /videos/<id>
@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_one_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400
    
    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404
    else:
        video_dict = video.to_dict()
     
    return jsonify({"video": video_dict}), 200


# POST /videos
@videos_bp.route("", methods=["POST"], strict_slashes=False)
# when it gets a POST request (from postman in our case), it calls this function:
def create_video():  

    # this will look at the http request received and give us the JSON in the body as a Python dictionary
    request_body = request.get_json()

    if not request_body.get("title") or not request_body.get("release_date") \
        or not request_body.get("total_inventory"):
        return jsonify({"details": "Invalid data"}), 400 
    
    # make new video:
    new_video = Video(title = request_body["title"], \
        release_date = request_body["release_date"], \
            total_inventory = request_body["total_inventory"])

    db.session.add(new_video)   # this tells SQLAlchemy to add this new_book/model to the db (like staging, can stage multiple items)
    db.session.commit()     # this tells SQLAlchemy to commit the stages and make it happen (doing the action)

    # we need an extra step to transfer completed_at to is_completed:
    video_dict = new_video.to_dict()

    return jsonify({"video": video_dict}), 201


# PUT /videos/<id>
@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_single_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400
    
    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404

    form_data=request.get_json()

    if not form_data.get("title") or not form_data.get("release_date") \
        or not form_data.get("total_inventory"):
        return jsonify({"details": "Invalid data"}), 400 

    video.title=form_data["title"]
    video.release_date=form_data["release_date"]
    video.total_inventory=form_data["total_inventory"]
    db.session.commit()

    # we need an extra step to transfer completed_at to is_completed:
    video_dict = video.to_dict()
    
    return jsonify({"video": video_dict}), 200


# DELETE /videos/<id>
@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400

    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404
   
    db.session.delete(video)
    db.session.commit()

    return jsonify({"details": f'Video {video.id} "{video.title}" successfully deleted'}), 200

