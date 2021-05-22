from flask import Blueprint, request, make_response, jsonify
from sqlalchemy import asc, desc
from app import db
from app.models.customer import Customer
from app.models.video import Video 
from app.models.rental import Rental
from datetime import datetime
import requests
import os
import random


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


#=====================================================#
#                  CUSTOMER ROUTES                    #
#=====================================================#


@customers_bp.route("", methods=["GET"])
def get_list_all_customers():
    """
    Get all Customers in asc, desc, or unsorted order
    """
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        customers = Customer.query.order_by(asc("name"))
    elif sort_query == "desc":
        customers = Customer.query.order_by(desc("name"))
    else:
        customers = Customer.query.all()

    customers_response = [customer.to_json() for customer in customers]

    return jsonify(customers_response)


@customers_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    """
    Get one Customer by id
    """
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("Customer not found", 404)

    customer_response = customer.to_json()
    return customer_response


@customers_bp.route("", methods=["POST"])
def add_new_customer():
    """
    Create a new Customer
    """
    request_body = request.get_json()

    try:
        request_body["name"]
        request_body["postal_code"]
        request_body["phone"]
    except:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    new_customer = Customer(name=request_body["name"],
                    postal_code=request_body["postal_code"],
                    phone=request_body["phone"])

    db.session.add(new_customer)
    db.session.commit()

    return make_response({"id": new_customer.customer_id}, 201)


@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer_by_id(customer_id):
    """ 
    Update one Customer by id
    """
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("Customer not found", 404)

    request_body = request.get_json()
    try:
        request_body["name"]
        request_body["postal_code"]
        request_body["phone"]
    except:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()

    return make_response(customer.to_json(), 200)


@customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id):
    """
    Delete one Customer by id
    """
    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response("Customer not found", 404)
    
    db.session.delete(customer)
    db.session.commit()

    return make_response({
        "id": customer_id
    })


#=====================================================#
#                     VIDEO ROUTES                    #
#=====================================================#


@videos_bp.route("", methods=["GET"])
def get_list_all_videoss():
    """
    Get all Videos in asc, desc, or unsorted order
    """
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        videos = Video.query.order_by(asc("name"))
    elif sort_query == "desc":
        videos = Video.query.order_by(desc("name"))
    else:
        videos = Video.query.all()

    videos_response = [video.to_json() for video in videos]

    return jsonify(videos_response)


@videos_bp.route("/<int:video_id>", methods=["GET"])
def get_video_by_id(video_id):
    """
    Get one Video by id
    """
    video = Video.query.get(video_id)

    if video is None:
        return make_response("Video not found", 404)

    video_response = video.to_json()
    return video_response

@videos_bp.route("", methods=["POST"])
def add_new_video():
    """
    Create a new Video
    """
    request_body = request.get_json()

    try:
        request_body["title"]
        request_body["release_date"]
        request_body["total_inventory"]
    except:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    new_video = Video(title=request_body["title"],
                    release_date=request_body["release_date"],
                    total_inventory=request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit()

    return make_response({"id": new_video.video_id}, 201)


@videos_bp.route("/<int:video_id>", methods=["PUT"])
def update_video_by_id(video_id):
    """ 
    Update one Video by id
    """
    video = Video.query.get(video_id)

    if video is None:
        return make_response("Video not found", 404)

    request_body = request.get_json()
    try:
        request_body["title"]
        request_body["release_date"]
        request_body["total_inventory"]
    except:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.commit()

    return make_response(video.to_json(), 200)


@videos_bp.route("/<int:video_id>", methods=["DELETE"])
def delete_video_by_id(video_id):
    """
    Delete one Video by id
    """
    video = Video.query.get(video_id)

    if video is None:
        return make_response("Video not found", 404)
    
    db.session.delete(video)
    db.session.commit()

    return make_response({
        "id": video_id
    })


#=====================================================#
#                   RENTAL ROUTES                     #
#=====================================================#


@rentals_bp.route("/check-out", methods=["POST"])
def add_rental_to_customer():
    """
    Check-out a new Rental
    """
    request_body = request.get_json()

    try:
        # request_body["customer_id"]
        # request_body["video_id"]
        # isinstance(request_body["customer_id"], int)
        # isinstance(request_body["video_id"], int)
        request_body["customer_id"]=int(request_body["customer_id"])
        request_body["video_id"]=int(request_body["video_id"])
        # video.available_inventory > 0
    except:
        return make_response({
            "details": "Invalid data"
        }, 400)

    customer = Customer.query.get_or_404(request_body["customer_id"])
    video = Video.query.get_or_404(request_body["video_id"])

    customer.videos_checked_out_count += 1
    video.available_inventory -= 1

    if video.available_inventory < 0: 
        return make_response(jsonify({
            "error": "No available inventory"
        }), 400)

    new_rental = Rental(customer_id=request_body["customer_id"],
                    video_id=request_body["video_id"])
    db.session.add(new_rental)
    db.session.commit()

    return make_response({
        "customer_id": new_rental.customer_id,
        "video_id": new_rental.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }, 200)


@rentals_bp.route("/check-in", methods=["POST"])
def customer_returns_rental():
    """
    Return an active Rental
    """
    request_body = request.get_json()
    # rental = Rental.query.filter_by(video_id=request_body["video_id"],customer_id=request_body["customer_id"]).one_or_none()
    # rental = Rental.query.get((request_body["customer_id"],request_body["video_id"]))
    # get the rental id thru query filter 
    # drop that rental 
    # customer.videos_checked_out_count -= 1
    # video.available_inventory += 1

    # if video.available_inventory < 1:
    #     return make_response(jsonify({
    #         "details": "Invalid data"
    #     }), 400)
    try:
        customer_id = int(request_body["customer_id"])
        video_id = int(request_body["video_id"])
        # video.available_inventory < video.total_inventory
        # video.available_inventory < 1
        # rental != None
    except ValueError or KeyError:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    customer = Customer.query.get_or_404(request_body["customer_id"])
    video = Video.query.get_or_404(request_body["video_id"])
    # rental = Rental.query.get((request_body["customer_id"],request_body["video_id"]))
    rental = Rental.query.filter_by(video_id=request_body["video_id"],customer_id=request_body["customer_id"]).one_or_none()
    if rental is None: 
        return make_response(jsonify({
            "details": "Invalid data" }), 400)

    customer.videos_checked_out_count -= 1
    video.available_inventory += 1
    db.session.delete(rental)
    db.session.commit()

    return make_response({
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }, 200)

# do i put this route in custmer routes?? 
@customers_bp.route("/<int:customer_id>/rentals", methods=["GET"])
def get_all_current_rentals_by_id(customer_id):
    """
    Get all the Videos a specific Customer currently has checked out 
    """
    customer = Customer.query.get(customer_id)

    # rentals should be all the instances of videos checked out by customer id?? 
    # rentals = db.session.query(Customer, Video, Rental).join(Customer,Customer.customer_id==Rental.customer_id).join(Video, Video.video_id==Rental.video_id).filter(Customer.customer_id == customer_id).all()
    # print(type(rentals)) # returned a list 
    # print(rentals)
    # get all the rentals?
    rentals = customer.videos
    print(rentals) # this is a list of objects of rental class! thats why to_json
    rentals_list = []
    # create a list called rentals_response and list comprehension here
    # there is not to_json() for this object-- what is rentals a object of? not video?? 
    # rentals_response = [rental for rental in rentals]
    for rental in rentals: 
        video = Video.query.get(rental.video_id)
        rentals_list.append({"title":video.title,
                            "due_date":rental.due_date,
                            "release_date":video.release_date})

    return jsonify(rentals_list)


# do i put this route in video routes?? 
@videos_bp.route("/<int:video_id>/rentals", methods=["GET"])
def get_all_current_rentals_by_id(video_id):
    """
    Get all the Customers who currently have a specific Video checked out 
    """
    video = Video.query.get(video_id)
    renters = video.customers
    # print(rentals) # this is a list of objects of rental class! thats why to_json

    customers_list = []
    for renter in renters: 
        customer = Customer.query.get(renter.customer_id)
        customers_list.append({"name":customer.name,
                            "due_date":renter.due_date,
                            "phone":customer.phone,
                            "postal_code":customer.postal_code})

    return jsonify(customers_list)

