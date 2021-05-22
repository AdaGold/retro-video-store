from app import db
from flask import Blueprint
from .models.customer import Customer
from .models.video import Video
from .models.rental import Rental
from flask import request
from flask import jsonify, make_response
from sqlalchemy import asc, desc 
# import requests
# import os

# creating instance of the model, first arg is name of app's module
customer_bp = Blueprint("customers", __name__, url_prefix="/customers") 
video_bp = Blueprint("videos", __name__, url_prefix="/videos") 
rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals") 

#create a customer with null completed at
@customer_bp.route("", methods = ["POST"], strict_slashes = False)
def create_customer():
    try:
        request_body = request.get_json()
        new_customer = Customer.from_json_to_customer(request_body)
        db.session.add(new_customer) 
        db.session.commit() 
        return jsonify(id = new_customer.id), 201
    except KeyError:
        return {"details": "Bad Request"}, 400

# Retrieve all /customers  
@customer_bp.route("", methods = ["GET"], strict_slashes = False)
def retrieve_customers_data():
    customers = Customer.query.all() 
    customers_response = []
    if customers != None:  
        customers_response = [customer.customer_to_json_response() \
                for customer in customers]
    return jsonify(customers_response), 200

# Retrieve one /customers/1     
@customer_bp.route("/<customer_id>", methods=["GET"], strict_slashes = False)
def retrieve_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer == None:
        return make_response('Not Found', 404)
    return customer.customer_to_json_response(), 200

#Update a customer
@customer_bp.route("/<customer_id>", methods=["PUT"], strict_slashes = False)  
def update_customer(customer_id):
    customer = Customer.query.get(customer_id) #SQL ALCHEMY QUERY
    # if quering customer with given customer_id, not succesful send error
    if not customer:
        return jsonify("Not Found"), 404 
    form_data = request.get_json() 

    # if quering customer doesn't contain all needed fields, send error
    if not "name" in form_data or not "postal_code" in form_data \
        or not "phone" in form_data:
        return jsonify("Bad Request"), 400

    # Otherwise, make the changes: 
    customer.name = form_data["name"]
    customer.postal_code = form_data["postal_code"]
    customer.phone = form_data["phone"]
    db.session.commit() 
    return customer.customer_to_json_response(), 200 

# Delete a customer
@customer_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes = False)
def delete_customer(customer_id):  
    customer = Customer.query.get(customer_id) 
    # if quering customer doesn't return a valid customer, send error
    if customer == None:
        return jsonify("Not Found"), 404
    db.session.delete(customer)
    db.session.commit()
    details_str = f"Customer {customer_id} \"{customer.name}\" successfully deleted"
    return jsonify(id = customer.id, details = details_str), 200

## VIDEO ROUTES:
#create a video 
@video_bp.route("", methods = ["POST"], strict_slashes = False)
def create_video():
    try:
        request_body = request.get_json()
        new_video = Video.from_json_to_video(request_body)
        db.session.add(new_video) 
        db.session.commit() 
        details_str = f"Video \"{new_video.title}\" successfully created"
        return jsonify(id = new_video.id, details = details_str), 201
    except KeyError:
        return {"details": "Bad Request"}, 400

# Retrieve all /videos  
@video_bp.route("", methods = ["GET"], strict_slashes = False)
def retrieve_videos_data():
    videos = Video.query.all() 
    videos_response = []
    if videos != None:  
        videos_response = [video.video_to_json_response() \
                for video in videos]
    return jsonify(videos_response), 200

# Retrieve one /videos/1     
@video_bp.route("/<video_id>", methods=["GET"], strict_slashes = False)
def retrieve_single_video(video_id):
    video = Video.query.get(video_id)
    if video == None:
        return make_response('Not Found', 404)
    return video.video_to_json_response(), 200

#Update a video
@video_bp.route("/<video_id>", methods=["PUT"], strict_slashes = False)  
def update_video(video_id):
    video = Video.query.get(video_id) 
    form_data = request.get_json()
    # if quering video with given video_id not succesful, send error
    if not video:
        return jsonify("Not Found"), 404 
    # if quering video doesn't contain all needed fields succesful send error
    if not form_data or not ("title" in form_data) or not ("release_date" in form_data) \
        or not ("total_inventory" in form_data):
        return jsonify("Bad Request"), 400

    # Otherwise, make the changes: 
    video.title = form_data["title"]
    video.release_date = form_data["release_date"]
    video.total_inventory = form_data["total_inventory"]
    
    db.session.commit() 
    return video.video_to_json_response(), 200 

# Delete a video
@video_bp.route("/<video_id>", methods=["DELETE"], strict_slashes = False)
def video_customer(video_id):  
    video = Video.query.get(video_id) 
    # if quering customer doesn't return a valid customer, send error
    if video == None:
        return jsonify("Not Found"), 404
    db.session.delete(video)
    db.session.commit()
    details_str = f"Video {video_id} \"{video.title}\" successfully deleted"
    return jsonify(id = video.id, details = details_str), 200

## RENTAL ROUTES:
#checks out a video 
@rental_bp.route("/check-out", methods = ["POST"], strict_slashes = False)
def check_out_video():

    try:
        request_body = request.get_json()
        video = Video.query.get(request_body["video_id"])
        customer = Customer.query.get(request_body["customer_id"])

        if not video or not customer: 
            return {"details": "Not Found"}, 404
        elif video.available_inventory < 1: # need to check if inv is lower than
            return {"details": "Bad Request"}, 400
        else:
        # once all fields valid, will create rental and update due date
            new_rental = Rental.from_json_to_check_out(request_body)
            customer.videos_checked_out_count += 1
            video.available_inventory -= 1

            db.session.add(new_rental) 
            db.session.commit() 

            return {"customer_id": customer.id,
                    "video_id": video.id,
                    "due_date": new_rental.due_date.strftime("%a, %d %b %Y %X %z %Z"),
                    "videos_checked_out_count": customer.videos_checked_out_count,
                    "available_inventory": video.available_inventory}, 200
    except:
        return {"details": "Bad Request"}, 400

#checks in a video 
@rental_bp.route("/check-in", methods = ["POST"], strict_slashes = False)
def check_in_video():
    try:
        request_body = request.get_json() 
        # Querying by customer_id and video_id with given info
        video = Video.query.get(request_body["video_id"])
        customer = Customer.query.get(request_body["customer_id"])
        # filters first video  by video id, that matches customer id query
        rental = Rental.query.filter(Customer.id == customer.id)\
            .filter(Video.id == video.id).first()
        # print(rental)
        # if  customer or video don't exist, 404
        if not video or not customer: 
            return {"details": "Not Found"}, 404
        # need to check if video id is in rental
        elif not "video_id" in request_body or \
            not "customer_id" in request_body: 
            return {"details": "Bad Request"}, 400
        elif not rental:
            return {"details": "Bad Request"}, 400
        elif customer.videos_checked_out_count < 1:
            return {"details": "Bad Request"}, 400
        else:
        # once all fields valid, will create rental and update due date
            new_rental = Rental.from_json_to_check_out(request_body)
            customer.videos_checked_out_count -= 1
            video.available_inventory += 1
            db.session.add(new_rental) 
            db.session.commit() 

            return {"customer_id": customer.id,
                    "video_id": video.id,
                    "videos_checked_out_count": customer.videos_checked_out_count,
                    "available_inventory": video.available_inventory}, 200
    except:
        return {"details": "Bad Request"}, 400

###  GET /customers/<id>/rentals
### list videos a customer currently has checked out
@customer_bp.route("/<customer_id>/rentals", methods = ["GET"], \
    strict_slashes = False)
def retrieve_videos_checked_out_by_customer(customer_id):
    customer = Customer.query.get(customer_id) # querying customer by given id
    if customer == None:
        return jsonify('Not Found'), 404
    # an instance of rentals including (rental id, customer_id, video_id, 
    # rental_date and due_date), queried by customer id. 
    rentals = Rental.query.filter(Rental.customer_id==customer_id).all()
    # print(rentals)
    videos_checked_out = []
    for rental in rentals:
    # to query (instead of joining tables) with its instance of all the videos 
    # for that customer including (id, title, release date, total inventory,
    # available inventory)
        video = Video.query.get(rental.video_id)
        videos_checked_out.append(Rental.customer_rentals_response(rental, video)) 
    return jsonify(videos_checked_out), 200

@video_bp.route("/<video_id>/rentals", methods = ["GET"], \
    strict_slashes = False)

### list customer details with due date for video checked out
def retrieve_customers_that_checked_out_video(video_id):
    video = Video.query.get(video_id) # querying video by given id
    if video == None:
        return jsonify('Not Found'), 404
    # instance of rentals with (rental id, customer_id, video_id, 
    # rental_date and due_date), queried by video_id
    rentals = Rental.query.filter(Rental.video_id==video_id).all()
    customers_due_date = []
    for rental in rentals:
        customer = Customer.query.get(rental.customer_id)
        customers_due_date.append(Rental.customer_due_date_response(rental, \
            customer)) 
    return jsonify(customers_due_date), 200

