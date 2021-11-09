import datetime
from typing import ChainMap
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import requests

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")
customer_bp = Blueprint("customer_bp", __name__, url_prefix="/customers")
rental_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")


#----------------------------------------------------------------------------------#
#---------------------------  Customer Endpoints    -------------------------------#
#----------------------------------------------------------------------------------#
customer_keys = ["name", "phone", "postal_code"]

@customer_bp.route("", methods=["GET"]) 
def read_customers():
    customer_response = []
    customers = sort_titles(request.args.get("sort"), Customer)
    customer_response = [customer.to_dict() for customer in customers]
    return jsonify(customer_response), 200

@customer_bp.route("", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    check = check_customer_video_data(method="POST", 
                            request_body=request_body, 
                            keys=customer_keys)
    return check if check else create_customer(request_body)

@customer_bp.route("/<customer_id>", methods=["GET"])
def read_a_customer(customer_id):
    check = check_customer_video_data(method="GET", 
                            id=customer_id, 
                            model=Customer, 
                            entity="Customer")
    return check if check else make_response(Customer.query.get(customer_id).to_dict(),200)

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_a_customer(customer_id):
    check = check_customer_video_data(method="DELETE", 
                            id=customer_id, 
                            model=Customer,
                            entity="Customer")
    if check:
        return check
    customer = Customer.query.get(customer_id)
    db.session.delete(customer)
    db.session.commit()
    response = {"id": customer.id}
    return make_response(response, 200)

@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_a_customer(customer_id):
    request_body = request.get_json()
    check = check_customer_video_data(method="PUT", 
                            request_body=request_body, 
                            id=customer_id, 
                            model=Customer, 
                            entity="Customer", 
                            keys=customer_keys)
    if check:
        return check
    customer = Customer.query.get(customer_id)
    customer.name = request_body["name"]
    customer.phone = request_body["phone"]
    customer.postal_code = request_body["postal_code"]
    db.session.commit()
    return make_response(customer.to_dict(), 200)

@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def read_rentals_by_customer(customer_id):
    check = check_customer_video_rental_data(id=customer_id, 
                                                model=Customer, 
                                                entity="Customer", 
                                                method="GET")
    if check:
        return check
    rentals = db.session.query(Rental).filter(Rental.customer_id==customer_id)
    videos=[Video.query.get(rental.video_id) for rental in rentals]
    rental_response = [video.to_dict() for video in videos]
    return jsonify(rental_response), 200

#----------------------------------------------------------------------------------#
#---------------------------   Video Endpoints      -------------------------------#
#----------------------------------------------------------------------------------#

video_keys = ["title", "release_date", "total_inventory"]

@video_bp.route("", methods=["GET"])
def read_videos():
    videos_response = []
    #this part can go in a helper function, we can also create sort by release date
    # if request.args.get("sort") == "asc": 
    #     videos = Video.query.order_by(Video.title.asc())
    # elif request.args.get("sort") == "desc":
    #     videos = Video.query.order_by(Video.title.desc())
    # else:
    #     videos = Video.query.all()
    videos = sort_titles(request.args.get("sort"), Video)
    #print(videos)
    videos_response = [video.to_dict() for video in videos]
    return jsonify(videos_response), 200

@video_bp.route("", methods=["POST"])
def create_video():
    request_body = request.get_json()
    check = check_customer_video_data(method="POST", 
                                        request_body=request_body, 
                                        keys=video_keys)
    return check if check else create_video(request_body)

@video_bp.route("/<video_id>", methods=["GET"])
def read_a_video(video_id):
    check = check_customer_video_data(method="GET", 
                                        id=video_id, 
                                        model=Video, 
                                        entity="Video")
    return check if check else make_response(Video.query.get(video_id).to_dict(),200)

@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    request_body = request.get_json()
    check = check_customer_video_data(method="PUT", 
                                        request_body=request_body, 
                                        id=video_id, 
                                        model=Video, 
                                        entity="Video", 
                                        keys=video_keys)
    if check:
        return check
    video = Video.query.get(video_id) 
    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]
    db.session.commit()
    return make_response(video.to_dict(), 200)
    
@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    check = check_customer_video_data(method="DELETE", 
                                        id=video_id, 
                                        model=Video,
                                        entity="Video")
    if check:
        return check
    video = Video.query.get(video_id) 
    db.session.delete(video)
    db.session.commit()
    response = {"id": video.id}
    return make_response(response, 200)

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def read_rentals_by_video(video_id):
    check = check_customer_video_rental_data(id=video_id, 
                                                model=Video, 
                                                entity="Video", 
                                                method="GET")
    if check:
        return check
    rentals = db.session.query(Rental).filter(Rental.video_id==video_id)
    customers=[Customer.query.get(rental.customer_id) for rental in rentals]
    rental_response = [customer.to_dict() for customer in customers]
    return jsonify(rental_response), 200

#----------------------------------------------------------------------------------#
#---------------------------   Rental Endpoints     -------------------------------#
#----------------------------------------------------------------------------------#
rental_keys = ["customer_id", "video_id"]

@rental_bp.route("/check-out", methods=["POST"])
def handle_check_out():
    request_body = request.get_json()
    check = check_customer_video_rental_data(request_body=request_body, method="POST")
    if check:
        return check
    else: 
        video_id = request_body["video_id"]
        video = Video.query.get(video_id)
        inventory_available = calculate_inventory_available(video)
        if inventory_available > 0:
            video.inventory_checked_out += 1
            inventory_available = calculate_inventory_available(video)
            today = datetime.now(timezone.utc)
            RENTAL_PERIOD = 7
            due_date = today + timedelta(days=RENTAL_PERIOD)
            new_rental = create_rental(request_body, due_date) # Replaced the code below with helper function like for video and customer
            # new_rental = Rental(
            # video_id=video_id, 
            # customer_id=customer_id, 
            # due_date=due_date)
            # db.session.add(new_rental)
            # db.session.commit()
            return make_response(new_rental.to_dict(checked_out=video.inventory_checked_out, available_inventory=inventory_available), 200)
        else:
            return make_response({"message": "Could not perform checkout"}, 400)

@rental_bp.route("/check-in", methods=["POST"])
def handle_check_in():
    request_body = request.get_json() 
    check =check_customer_video_rental_data(request_body=request_body, method="POST")
    if check:
        return check
    else:
        video_id = request_body["video_id"]
        customer_id = request_body["customer_id"]
        video = Video.query.get(video_id)
        video.inventory_checked_out -= 1
        inventory_available = calculate_inventory_available(video)
        rentals = Rental.query.filter(Rental.customer_id==customer_id).all() 
        result = make_response({'message': f"No outstanding rentals for customer {customer_id} and video {video_id}"}, 400)
        if not rentals:
            #return a not found type message?
            return result  
        for rental in range(len(rentals)):
            if rentals[rental].video_id == video_id:
                result = make_response(rentals[rental].to_dict(checked_out=video.inventory_checked_out, available_inventory=inventory_available), 200)
                db.session.delete(rentals[rental])
                db.session.commit()
        return result



#----------------------------------------------------------------------------------#
#---------------------------    Helper Functions    -------------------------------#
#----------------------------------------------------------------------------------#
def create_customer(request_body):
        new_customer = Customer(name=request_body["name"],
                            phone=request_body["phone"], 
                            postal_code=request_body["postal_code"],
                            register_at=datetime.utcnow())
        db.session.add(new_customer)
        db.session.commit()
        return make_response(new_customer.to_dict(), 201)

def create_video(request_body):
    new_video = Video(title=request_body["title"],
                            release_date=request_body["release_date"], 
                            total_inventory=request_body["total_inventory"])
    db.session.add(new_video)
    db.session.commit()
    return make_response(new_video.to_dict(), 201)

def create_rental(request_body, due_date):
    new_rental = Rental(video_id=request_body["video_id"], 
                        customer_id=request_body["customer_id"], 
                        due_date=due_date)
    db.session.add(new_rental)
    db.session.commit()
    return new_rental

def sort_titles(sort_by, entity):
    #Thinking about making this a very generic function to sort anything with a simple order_by 
    if sort_by == "asc": 
        sorted = entity.query.order_by(entity.title.asc())
    elif sort_by == "desc":
        sorted = entity.query.order_by(entity.title.desc())
    else:
        sorted = entity.query.all()
    return sorted

def sort_dates(sort_by):
    #May want to use this for release_dates if sort_titles can'st be made generic?
    pass 


def check_customer_video_data(method=None, request_body=None, keys=None, id=None, model=None, entity=None):
    if method == "POST":
        for key in keys:
            if key not in request_body.keys():
                return make_response({"details": f"Request body must include {key}."}, 400)
        return False
    elif method == "GET" or method == "DELETE":
        if not id.isnumeric():
            response = make_response({"message" : "Please enter a valid customer id"}, 400)
        elif not model.query.get(id):
            response = make_response({"message" : f"{entity} {id} was not found"}, 404)
        else:
            response = False
        return response
    elif method == "PUT":
        if not id.isnumeric():
            response = make_response({"message" : "Please enter a valid customer id"}, 400)
        elif not model.query.get(id):
            response = make_response({"message" : f"{entity} {id} was not found"}, 404)
        else:
            response = False
        for key in keys:
            if key not in request_body.keys():
                response = make_response({"details": f"Request body must include {key}."}, 400)
        return response

def check_customer_video_rental_data(id=None, model=None, entity=None, method=None, request_body=None):
    if method == "GET":
        if not id.isnumeric():
            return make_response({"message" : "Please enter a valid customer id"}, 400)
        elif not model.query.get(id):
            return make_response({"message" : f"{entity} {id} was not found"}, 404)
        else:
            return False
    elif method == "POST":
        if "video_id" not in request_body.keys() or "customer_id" not in request_body.keys():
            return make_response({"details": "Please enter a valid customer id AND video id"}, 400)
        video = Video.query.get(request_body["video_id"])
        customer = Customer.query.get(request_body["customer_id"])
        if not video or not customer:
            return make_response({"details": "The video or customer id you have entered is incorrect"}, 404)
        else:
            return False

def calculate_inventory_available(video):
    return video.total_inventory - video.inventory_checked_out

#DRY for error checks: https://stackoverflow.com/questions/38488476/a-dry-approach-to-python-try-except-blocks
# def check_rental_data(request_body): 
#     # I think maybe the not_found_response() function and check_data() function could be combined into something similar to this? 
#     # At least in my customer functions, i have a lot of repetative "if response: return response"
#     if "video_id" not in request_body.keys() or "customer_id" not in request_body.keys():
#         return make_response({"details": "Please enter a valid customer id AND video id"}, 400)
#     video = Video.query.get(request_body["video_id"])
#     customer = Customer.query.get(request_body["customer_id"])
#     if not video or not customer:
#         return make_response({"details": "The video or customer id you have entered is incorrect"}, 404)
#     # if video.total_inventory == 0 or video.total_inventory is None:
#     #     return make_response({"message": "Could not perform checkout"}, 400) 
#     return False

# def not_found_response(entity, id): 
#     return make_response({"message" : f"{entity} {id} was not found"}, 404)

# def id_check(id):
#     response = make_response({"message" : "Please enter a valid customer id"}, 400)
#     return response if not id.isnumeric() else False

# def check_data(check_items, request_body): 
#     for key in check_items:
#         if key not in request_body.keys():
#             return make_response({"details": f"Request body must include {key}."}, 400)
#     return False

# def create_check_out(request_body):
#     video_id = request_body["video_id"]
#     customer_id = request_body["customer_id"]
#     video = Video.query.get(video_id)
#     customer = Customer.query.get(customer_id)
#     if video.total_inventory > 0:
#         video.inventory_checked_out += 1
#         inventory_available = video.total_inventory - video.inventory_checked_out
#     else: 
#         return make_response({"message": "Could not perform checkout"}, 400)
    
#     today = datetime.now(timezone.utc)
#     RENTAL_PERIOD = 7
#     due_date = today + timedelta(days=RENTAL_PERIOD)
    
#     new_rental = Rental(video_id=video_id, customer_id=customer_id, due_date=due_date)
#     db.session.add(new_rental)
#     db.session.commit()
#     return make_response(new_rental.to_dict(checked_out=video.inventory_checked_out, available_inventory=inventory_available), 200)

# def create_check_in(request_body):
#     video_id = request_body["video_id"]
#     customer_id = request_body["customer_id"]
#     video = Video.query.get(video_id)
#     video.inventory_checked_out-=1
#     inventory_available = video.total_inventory - video.inventory_checked_out
#     rental = Rental.query.get()
#     db.session.delete(rental)
#     db.session.commit()
#     return make_response(rental.to_dict(checked_out=video.inventory_checked_out, available_inventory=inventory_available), 200)
