from app import db
from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
# from sqlalchemy import desc, asc 
from datetime import datetime, timedelta, date
import requests
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customers_response = [customer.to_dict() for customer in customers]
    return jsonify(customers_response)

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return customer.to_dict()
    return (f"No customer with ID #{customer_id} found", 404)

@customers_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    if valid_customer_input(request_body):
        new_customer = Customer(name = request_body["name"],
                        postal_code = request_body["postal_code"],
                        phone = request_body["phone"])
        new_customer.registered_at = datetime.utcnow()
        db.session.add(new_customer)
        db.session.commit()
        # WHY isn't this working with Wave1 tests??
        # return (new_customer.to_dict(), 201)
        return ({"id": new_customer.customer_id}, 201) 
    return ({"details": "Invalid data"}, 400)

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    # need to include a way to return 400 error if 
    # any of the request body fields are missing or invalid
    # (or example if the videos_checked_out_count is not a number)
    customer = Customer.query.get(customer_id)
    if customer:
        form_data = request.get_json()
        if valid_customer_input(form_data):
            customer.name = form_data["name"]
            customer.postal_code = form_data["postal_code"]
            customer.phone = form_data["phone"]
            db.session.commit()
            return customer.to_dict()
            # return make_response((customer.to_dict()), 200)
        #probably need to get more specific with the 400 message
        return ({"details": "Invalid data"}, 400)
        # return ("Invalid input", 400)
    # return ("", 404)
    return (f"No customer with ID #{customer_id} found", 404)
    

# this function probably needs to be more detailed and
# might need to include check_out info, etc
# this function could be built out so it does...
# if not "name" in form_data
#   return ("specific details of error")
# consider moving this to the Video model...
def valid_customer_input(form_data):
    if "name" in form_data and "postal_code" in form_data and "phone" in form_data:
        return True 
    return False

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return make_response({"id": customer.customer_id}, 200)
    return make_response(f"No customer with ID #{customer_id} found", 404)


@videos_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    videos_response = [video.to_dict() for video in videos]
    return jsonify(videos_response)

@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    video = Video.query.get(video_id)
    if video:
        return video.to_dict()
    return (f"No video with ID #{video_id} found", 404)

@videos_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    if valid_video_input(request_body):
        new_video = Video(title = request_body["title"],
                        release_date = request_body["release_date"],
                        total_inventory = request_body["total_inventory"])
        new_video.available_inventory = new_video.total_inventory
        db.session.add(new_video)
        db.session.commit()
        return ({"id": new_video.video_id}, 201) 
    return ({"details": "Invalid data"}, 400)

# condsider moving this to the Video model
def valid_video_input(form_data):
    if "title" in form_data and "release_date" in form_data and "total_inventory" in form_data:
        return True 
    return False

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    # need to include a way to return 400 error if 
    # any of the request body fields are missing or invalid
    # (or example if the total_inventory is not a number)
    video = Video.query.get(video_id)
    if video:
        form_data = request.get_json()
        if valid_video_input(form_data):
            video.title = form_data["title"]
            video.release_date = form_data["release_date"]
            video.total_inventory = form_data["total_inventory"]
            # video.available_inventory = form_data["available_inventory"]
            db.session.commit()
            return video.to_dict()
            # return make_response((video.to_dict()), 200)
        #probably need to get more specific with the 400 message
        return ({"details": "Invalid data"}, 400)
        # return ("Invalid input", 400)
    # return ("", 404)
    return (f"No video with ID #{video_id} found", 404)

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video:
        db.session.delete(video)
        db.session.commit()
        return make_response({"id": video.video_id}, 200)
    return make_response(f"No video with ID #{video_id} found", 404)


# WAVE2 -- not working ???
@rentals_bp.route("/check-out", methods=["POST"])
def check_out_video_to_customer():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    # check for valid input of customer id and video id 
    if customer_id == None or not type(customer_id) is int:
        return ({"error": "Please provide a valid customer ID"}, 400)
    if video_id == None or not type(video_id) is int:
        return ({"error": "Please provide a valid video ID"}, 400)
    
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer == None:
        return ({"error": "Customer not found."}, 404)
    if video == None:
        return ({"error": "Video not found."}, 404)
    if video.available_inventory == 0:
        return ({"error": "No available inventory."}, 400)
    
    new_rental = Rental(customer_id = customer_id, 
                        video_id = video_id)
    new_rental.due_date = date.today() + timedelta(days=7)
    db.session.add(new_rental)
    customer.check_out()
    video.check_out()
    db.session.commit()
    # CONSIDER making a function that builds successful response body
    return make_response({"customer_id": customer.customer_id,
                "video_id": video.video_id,
                "due_date": new_rental.due_date,
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory}, 200)

# condsider moving this to the Rental model
# not currently being used .... 
def valid_rental_input(form_data):
    if "customer_id" in form_data and "video_id" in form_data:
        if type(form_data["customer_id"]) is int and type(form_data["video_id"]) is int:
            return True 
    return False

## FUNCTION NEEDS TO BE REWORKED to check that a rental exists ... 
@rentals_bp.route("/check-in", methods=["POST"]) 
def check_in_video():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    # check for valid input of customer id and video id 
    if customer_id == None or not type(customer_id) is int:
        return ({"error": "Please provide a valid customer ID"}, 400)
    if video_id == None or not type(video_id) is int:
        return ({"error": "Please provide a valid video ID"}, 400)
    
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)
    if customer == None:
        return ({"error": "Customer not found."}, 404)
    if video == None:
        return ({"error": "Video not found."}, 404)

    # check to see if rental with customer and video id exists
    # HOW TO DO THIS!?
    rental = Rental.query.get(customer_id)
    if rental == None:
        return ({"error": "Rental not found."}, 400)

    customer.check_in()
    video.check_in()
    db.session.commit()
    # CONSIDER making a function that builds successful response body
    return ({"customer_id": customer.customer_id,
                "video_id": video.video_id,
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory}, 200)









    # request_body = request.get_json()
    # # NEED TO CHECK THAT THERE IS A RENTAL with this info! 
    # #if valid rental input is true:
    # if valid_rental_input(request_body):
    #     #if customer_id and video_id and are valid and in the request:
    #     customer = Customer.query.get(request_body["customer_id"])
    #     video = Video.query.get(request_body["video_id"])
    #     if customer and video:
    #         customer.check_in()
    #         video.check_in()

    #         #do i need this line??
    #         db.session.commit()
    #         return ({"customer_id": customer.customer_id,
    #                     "video_id": video.video_id,
    #                     "videos_checked_out_count": customer.videos_checked_out_count,
    #                     "available_inventory": video.available_inventory}, 200)
    #     # else, return 404 error for not found
    #     return ({"details": "Customer or video does not exist"}, 400)
    # # else, return 400
    # return ({"details": "Invalid data"}, 400)