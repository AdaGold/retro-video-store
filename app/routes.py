from dataclasses import dataclass
from flask import Blueprint, json
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
from flask import request, Blueprint, make_response, Response, jsonify, render_template
from sqlalchemy import desc
from datetime import datetime, timedelta
import requests
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

##########################################################################################
#################################### CUSTOMERS CRUD ######################################
##########################################################################################

#1############ GET ALL CUSTOMERS - CRUD - READ #######################
@customers_bp.route("", methods=["GET"]) 
def get_all_customers():
    customers = Customer.query.all()
    customers_response = []
    for c in customers: 
        each_customer = c.to_dictionary()
        customers_response.append(each_customer)
    return jsonify(customers_response), 200

#2############ GET ONE CUSTOMER by ID - CRUD - READ ###################
@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    if not customer_id.isdigit():
        error_response2 = "is not a number"
        return jsonify(errors={"customer_id": error_response2}), 400

    customer = Customer.query.get(customer_id)
    if customer:
        return jsonify(customer.to_dictionary()), 200
    else:
        error_response1 = "can't be blank"
        return jsonify(errors={"customer_id": error_response1}), 404 

#3###################### POST CUSTOMER CRUD - CREATE ###################
@customers_bp.route("", methods=["POST"])
def add_new_customer():
    request_body = request.get_json() 

    input_errors = []
    if 'name' not in request_body.keys(): 
        blank_name = {"name": "can't be blank"}
        input_errors.append(blank_name)
    if 'postal_code' not in request_body.keys():
        blank_postal_code = {"postal_code": "can't be blank"}
        input_errors.append(blank_postal_code)
    if 'phone' not in request_body.keys():
        blank_phone = {"phone": "can't be blank"}
        input_errors.append(blank_phone)
    if input_errors:
        return jsonify(errors=input_errors), 400

    else:
        new_customer = Customer(name=request_body["name"],
                    registered_at=datetime.now(), 
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"])

        db.session.add(new_customer)
        db.session.commit()

        jsonable_new_customer = new_customer.to_dictionary()
        return jsonify(jsonable_new_customer), 201

#4############ PUT CUSTOMER by ID - CRUD - UPDATE #######################
@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    update_customer = Customer.query.get(customer_id)
    if update_customer is None:
        return jsonify(errors=["Not Found"]), 404

    request_body = request.get_json() 

    input_errors = []

    if 'name' not in request_body.keys() or request_body["name"] == None:
        blank_name = {"name": "can't be blank"}
        input_errors.append(blank_name)
    if 'postal_code' not in request_body.keys() or request_body["postal_code"] == None:
        blank_postal_code = {"postal_code": "can't be blank"}
        input_errors.append(blank_postal_code)
    if 'phone' not in request_body.keys() or request_body["phone"] == None:
        blank_phone = {"phone": "can't be blank"}
        input_errors.append(blank_phone)

    if input_errors:
        return jsonify(errors=input_errors), 400

    else:
        request_in_json = request.get_json()

        update_customer.name = request_in_json["name"]
        update_customer.postal_code = request_in_json["postal_code"]
        update_customer.phone = request_in_json["phone"]

        db.session.commit()
    
        jsonable_update_customer = update_customer.to_dictionary()
        print(jsonable_update_customer)
        return jsonify(jsonable_update_customer), 200

#5############ DELETE CUSTOMER by ID - CRUD - DELETE #######################
@customers_bp.route("/<customer_id>", methods=["DELETE"]) 
def delete_customer(customer_id):
    delete_customer = Customer.query.get(customer_id)
    if delete_customer is None:
        response = {"errors": ["Not Found"]}
        return jsonify(response), 404
    else:
        db.session.delete(delete_customer)
        db.session.commit()
        return jsonify(id=int(customer_id)), 200

##########################################################################################
#################################### VIDEOS CRUD #########################################
##########################################################################################

#1############ GET ALL VIDEOS - CRUD - READ #######################
@videos_bp.route("", methods=["GET"]) 
def get_all_videos():
    videos = Video.query.all()
    videos_response = []
    for v in videos: 
        each_video = v.to_dictionary()
        videos_response.append(each_video)
    return jsonify(videos_response), 200

#2############ GET ONE VIDEO by ID - CRUD - READ ###################
@videos_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    if not video_id.isdigit():
        error_response2 = "is not a number"
        return jsonify(errors={"video_id": error_response2}), 404

    video = Video.query.get(video_id)
    if video:
        return jsonify(video.to_dictionary()), 200
    else:
        error_response1 = "can't be blank"
        return jsonify(errors={"video_id": error_response1}), 404

#3###################### POST VIDEO CRUD - CREATE ###################
@videos_bp.route("", methods=["POST"])
def add_new_video():
    request_body = request.get_json() 

    input_errors = []
    if 'title' not in request_body.keys(): 
        blank_title = {"title": "can't be blank"}
        input_errors.append(blank_title)
    if 'release_date' not in request_body.keys():
        blank_release_date = {"release_date": "can't be blank"}
        input_errors.append(blank_release_date)
    if 'total_inventory' not in request_body.keys():
        blank_inventory = {"total_inventory": "can't be blank"}
        input_errors.append(blank_inventory)
    if input_errors:
        return jsonify(errors=input_errors), 400
    else:
        new_video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"],
            available_inventory=request_body["total_inventory"]
        )

        db.session.add(new_video)
        db.session.commit()

        jsonable_new_video = new_video.to_dictionary()
        return jsonify(jsonable_new_video), 201

#4############ PUT VIDEO by ID - CRUD - UPDATE #######################
@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    update_video = Video.query.get(video_id)
    if update_video is None:
        return jsonify(errors=["Not Found"]), 404

    request_body = request.get_json() 
    input_errors = []
    if 'title' not in request_body.keys(): 
        blank_title = {"title": "can't be blank"}
        input_errors.append(blank_title)
    if 'release_date' not in request_body.keys():
        blank_release_date = {"release_date": "can't be blank"}
        input_errors.append(blank_release_date)
    if 'total_inventory' not in request_body.keys():
        blank_inventory = {"total_inventory": "can't be blank"}
        input_errors.append(blank_inventory)

    if input_errors:
        return jsonify(errors=input_errors), 400

    else:
        request_in_json = request.get_json()

        update_video.title = request_in_json["title"]
        update_video.release_date = request_in_json["release_date"]
        update_video.total_inventory = request_in_json["total_inventory"]

        db.session.commit()
    
        jsonable_update_video = update_video.to_dictionary()
        print(jsonable_update_video)
        return jsonify(jsonable_update_video), 200

#5############ DELETE VIDEO by ID - CRUD - DELETE #######################
@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    delete_video = Video.query.get(video_id)
    if delete_video is None:
        response = {"errors": ["Not Found"]}
        return jsonify(response), 404
    else:
        db.session.delete(delete_video) # deletes the model from the database
        db.session.commit() # Save Action
        return jsonify(id=int(video_id)), 200

##########################################################################################
#################################### RENTALS CRUD ########################################
##########################################################################################

######################## POST RENTAL /rentals/check-out CRUD - CREATE ###################
@rentals_bp.route("/check-out", methods=["POST"])
def checkout_to_customer():
    
    request_body = request.get_json() 

    input_errors = []
    if 'customer_id' not in request_body.keys(): 
        blank_customer_id = {"customer_id": "can't be blank"}
        input_errors.append(blank_customer_id)
    if 'video_id' not in request_body.keys():
        blank_video_id = {"video_id": "can't be blank"}
        input_errors.append(blank_video_id)    

    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")

    if input_errors:
        return jsonify(errors=input_errors), 400
    # elif not input_errors:
    #     video_thats_rented = Video.query.get(video_id)
    #     if video_thats_rented.available_inventory == 0:
    #         return jsonify(errors=(f"{video_id.title} is out of stock")), 400
    else:
        # increase the customer's videos_checked_out_count by one
        # make a helper function in customer model?
        customer_who_rents_video = Customer.query.get(customer_id)
        customer_who_rents_video.videos_checked_out_count += 1

        # decrease the video's available_inventory by one 
        # make a helper function in video model?
        video_thats_rented = Video.query.get(video_id)
        video_thats_rented.available_inventory -= 1

        new_rental = Rental(
            customer_id=request_body.get("customer_id"),
            video_id=request_body.get("video_id"),
            check_out=datetime.now(),
            due_date=datetime.now() + timedelta(days=7)
        )     # create a due_date that is 7 days from the current date
    
        db.session.add(new_rental)
        db.session.commit()

        response = {
            'customer_id': new_rental.customer_id,
            'video_id': new_rental.video_id,
            'due_date': new_rental.due_date,
            'videos_checked_out_count': customer_who_rents_video.videos_checked_out_count,
            'available_inventory': video_thats_rented.available_inventory
            }

        return jsonify(response), 200
        # jsonable_new_rental = new_rental.to_dictionary()
        # return jsonify(jsonable_new_rental), 201

    # have a success response that includes keys: 
    # ['customer_id', 'video_id', 'due_date', 'videos_checked_out_count', 'available_inventory']);

######################## POST RENTAL /rentals/check-in CRUD - CREATE ###################
# @rentals_bp.route("/check-in", methods=["POST"])
# def checkedin_from_customer():
    # request_body = request.get_json() 
    # rental_return = Rental(customer_id=request_body["customer_id"],
    #                 video_id=request_body["video_id"],
    #                 check_in=datetime.now(check_in))

    # # decrease the customer's videos_checked_out_count by one
    # customer_update = Customer.query.get(rental_return.customer_id)
    # customer_update.videos_checked_out_count -= 1
    # # increase the video's available_inventory by one
    # video_update = Video.query.get(rental_return.video_id)
    # video_update.available_inventory += 1

######################## GET RENTAL /customers/<id>/rentals CRUD - READ ###################
# @rentals_bp.route("", methods=["GET"])
# def list_all_vidoes_customer_has_out():
#     # all_current_videos_w1_customer
#     pass
# [
#     {
#         "release_date": "Wed, 01 Jan 1958 00:00:00 GMT",
#         "title": "Vertigo",
#         "due_date": "Thu, 13 May 2021 19:27:47 GMT",
#     },
#     {
#         "release_date": "Wed, 01 Jan 1941 00:00:00 GMT",
#         "title": "Citizen Kane",
#         "due_date": "Thu, 13 May 2021 19:28:00 GMT",
#     }
# ]


######################## GET RENTAL /videos/<id>/rentals CRUD - READ ###################
# @rentals_bp.route("/videos/<id>/rentals", methods=["GET"])
# def list_all_customers_who_currently_have_video(video_id):
#     who_has_the_vid = video_id
#     customers_with_video = db.session.query(Video, Customer, Rental).join(Video, Video.id==Rental.video_id).join(Customer, Customer.id==Rental.customer_id).filter(Video.id == who_has_the_vid).all()
    # ^ result will be an array of tuples. Easch tuple will hold 
    # a Video instance, Bar instance, and a Rental instance 
    # (in the order they are listd in the query)
# [
#     {
#         "due_date": "Thu, 13 May 2021 21:36:38 GMT",
#         "name": "Edith Wong",
#         "phone": "(555) 555-5555",
#         "postal_code": "99999",
#     },
#     {
#         "due_date": "Thu, 13 May 2021 21:36:47 GMT",
#         "name": "Ricarda Mowery",
#         "phone": "(555) 555-5555",
#         "postal_code": "99999",
#     }
# ]