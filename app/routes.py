from app import db
from app.models.customer import Customer
#from app.models.rentals import Rental
from app.models.video import Video
from flask import json, request, Blueprint, make_response, jsonify, Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
import os
from dotenv import load_dotenv
import requests

load_dotenv()

customer_bp = Blueprint("customers", __name__, url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
#rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# CRUD CUSTOMERS
@customer_bp.route("", methods=["GET"])
def list_customers():
    """Retrieves all customers and their related data from database"""
    customers = Customer.query.all()
    print('customers: ', type(customers)) # list of customer objects

    list_of_customers = []
    if not customers:
        return jsonify(list_of_customers)
    for customer in customers: # for every Customer instance/object in the list of them
        print('WHAT D.TYPE IS CUSTOMER? ', type(customer))
        list_of_customers.append(customer.to_json())
        print('list of customers: ', list_of_customers) # list of dicts
    return jsonify(list_of_customers) # jsonified list of dicts;;;;; LJ -- double formatting???

@customer_bp.route("/<customer_id>", methods=["GET"])
def list_single_customer(customer_id):
    """Retrieves data of specific customer"""
    single_customer = Customer.query.get(customer_id)
    print('SINGLE CUSTOMER: ', single_customer)
    if not single_customer:
        return make_response({"details": f"There is no customer in the database with ID #{customer_id}"}, 404)

    print('before: ', type(single_customer.postal_code))
    single_customer.postal_code = int(single_customer.postal_code)
    print('after: ', type(single_customer.postal_code))

    return jsonify(single_customer.to_json())

@customer_bp.route("", methods=["POST"])
def create_customer():
    """Create a customer for the database"""
    request_body = request.get_json() # form data submitted by user; telling flask tht it expects http request to this endpoint to contain txt that's structured as json; read that txt and give to me in json format
    
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body: # checks key; this way only prevents if the key is missing from the user's info (lets you click continue even if you gave an empty str as your phone number)
        return make_response({"details": "Customer name, phone number and postal code must all be provided, and they must be strings"}, 400)
    
    # TAKE OFF REGISTER_AT LINE AND VIDEOS_CHECKED...LINE TO PASS TESTS...
    new_customer = Customer(name=request_body["name"],
    postal_code=request_body["postal_code"],
    phone_number=request_body["phone"],
    register_at=datetime.now()) #, # changing bc the customer is registered when theyre created; line used to be ' register_at=request_body["registered_at"], '
    #videos_checked_out_count=request_body["videos_checked_out_count"]) ## add all attr.s you want user to be able to add when creating their customer acct

    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.customer_id}, 201)

@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_single_customer(customer_id):
    """Updates data of specific customer"""
    single_customer = Customer.query.get(customer_id)
    
    if not single_customer:
        return make_response({"details": f"Cannot perform this function. There is no customer in the database with ID #{customer_id}"}, 404)
    
    request_body = request.get_json()
    # check for missing keys and that each value type is the appropriate data type (str)
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body: 
        return make_response({"details": "Customer name, phone number and postal code must all be provided."}, 400)
    elif (type(request_body["name"]) != str) or (type(request_body["postal_code"]) != int) or (type(request_body["phone"]) != str):
        return make_response({"details: Customer name and phone number must be strings. Postal code must be an integer."}, 400)
    #intified_postal_code = int(request_body["postal_code"])
    single_customer.name = request_body["name"]
    single_customer.postal_code = request_body["postal_code"] # intified_postal_code  THIS IS NOT READING AS AN INT EVEN THOUGH IT SHOULD...
    single_customer.phone_number = request_body["phone"]
    # commented out following only to pass tests...
    #single_customer.videos_checked_out_count = request_body["videos_checked_out_count"] # no line for register_at attr bc registration happens when customer's created

    db.session.commit()
    return jsonify(single_customer.to_json())

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_single_customer(customer_id):
    """Delete a specific customer from the database"""
    single_customer = Customer.query.get(customer_id)
    if not single_customer:
        return make_response({"details": f"Cannot perform this function. There is no customer in the database with ID #{customer_id}"}, 404)

    db.session.delete(single_customer)
    db.session.commit()
    return make_response({"id": single_customer.customer_id}, 200)

# CRUD VIDEOS
@video_bp.route("", methods=["GET"])
def list_videos():
    """Retrieves all videos and their related data from database"""
    videos = Video.query.all()
    list_of_videos = []
    
    if not videos:
        return jsonify(list_of_videos)
    
    for video in videos:
        list_of_videos.append(video.to_json())
    return jsonify(list_of_videos)

@video_bp.route("/<video_id>", methods=["GET"])
def list_single_video(video_id):
    """Retrieves data of specific video"""
    single_video = Video.query.get(video_id)
    
    if not single_video:
        return make_response({"details": f"There is no video in the database with ID #{video_id}"}, 404)
    return jsonify(single_video.to_json())

@video_bp.route("", methods=["POST"])
def create_video():
    """Create a video for the database"""
    request_body = request.get_json() # form data submitted by user

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body: # checks key; this way only prevents if the key is missing from the user's info (lets you click continue even if you gave an empty str as your phone number)
        return make_response({"details": "Video title, release date and total in inventory must all be provided, and they must be string, datetime and integer values, respectively."}, 400)

    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"], # offer this format when creating a video: "1981-08-12" and it'll turn it to datetime obj in response
                    total_inventory=request_body["total_inventory"]) #,   # set this to 0??? to address 'null should be 0' in postman test? 
                    # commented next line out for tests
                    #available_inventory=request_body["available_inventory"])

    db.session.add(new_video)
    db.session.commit()
    return make_response({"id": new_video.video_id}, 201)

@video_bp.route("/<video_id>", methods=["PUT"])
def update_single_video(video_id):
    """Updates data of a specific video"""
    single_video = Video.query.get(video_id)
    if not single_video:
        return make_response({"details": f"Cannot perform this function. There is no video in the database with ID #{video_id}"}, 404)

    request_body = request.get_json()
    # check for missing values and that each value type is the appropriate data type
    print(request_body) # {'title': 'The Matrix 5', 'release_date': '2021-08-12', 'total_inventory': 1, 'available_inventory': 0}
    print(type(request_body["release_date"])) # str

    ## CONVERT STR TO DATETIME HERE, THEN PROCESS IT IN THE FOLLOWING LINE
    request_body["release_date"] = datetime.fromisoformat(request_body["release_date"])
    print('TYPE: ', type(request_body["release_date"])) # checks that str is turned into datetime obj successfully
    

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body: # or "available_inventory" not in request_body:
        return make_response({"details": "Video title, release date and inventory counts must all be provided."}, 400)
    elif (type(request_body["title"]) != str) or (type(request_body["release_date"]) != datetime) or (type(request_body["total_inventory"]) != int): # or (type(request_body["available_inventory"]) != int):
        return make_response({"details": "Video title must be a string, release date must be a datetime object and inventory/available counts must both be integers."}, 400)
    else:
        single_video.title = request_body["title"]
        single_video.release_date = request_body["release_date"]
        single_video.total_inventory = request_body["total_inventory"]
        #single_video.available_inventory = request_body["available_inventory"]

        db.session.commit()
        return jsonify(single_video.to_json())

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_single_video(video_id):
    """Delete a specific video from the database"""
    single_video = Video.query.get(video_id)
    
    if not single_video:
        return make_response({"details": f"Cannot perform this function. There is no video in the database with ID #{video_id}"}, 404)

    db.session.delete(single_video)
    db.session.commit()
    return make_response({"id": single_video.video_id}, 200) 

# # CRUD RENTALS ???
# @rental_bp.route("/check-out", methods=["POST"])
# def create_rental():
#     """Check out a video to a customer, re-creating it as a rental in the process"""
#     request_body = request.get_json() # employee scanning the movie the customer wants to take home

#     video_turned_rental = Rental(customer_id=request_body["customer_id"],
#                                 video_id=request_body["video_id"],
#                                 check_out_date=datetime.now()) #
#     return jsonify(video_turned_rental.to_json())


