from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
from datetime import datetime, timedelta
import requests
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route("", methods= ["GET", "POST"])
def handle_get_customers():
    if request.method == "GET":
        customers = Customer.query.all()
        get_response =[]
        for customer in customers:
            get_response.append(customer.make_json())
        return jsonify(get_response)

    elif request.method == "POST":
        request_body = request.get_json()
        
        if "name" not in request_body.keys() or "postal_code" not in \
            request_body.keys() or "phone" not in request_body.keys():
            return make_response({"details": "Invalid data"}, 400)
        
        new_customer = Customer(name=request_body["name"],\
            postal_code=request_body["postal_code"], phone_number=request_body["phone"],\
                register_at=datetime.now())
        
        db.session.add(new_customer)
        db.session.commit()
        return make_response(new_customer.make_json(), 201)

@customers_bp.route("/<id>", methods = ["GET", "PUT", "DELETE"])
def handle_customer(id):
    customer = Customer.query.get(id)

    if customer is None:
        return make_response("", 404)

    elif request.method == "GET":
        return customer.make_json()
    
    elif request.method == "PUT":
        request_body = request.get_json()
        
        if "name" not in request_body.keys() \
            or "postal_code" not in request_body.keys() \
                or "phone" not in request_body.keys() \
                    or not isinstance(request_body["name"], str) \
                        or not isinstance(request_body["postal_code"], int) \
                            or not isinstance(request_body["phone"], str):
                return make_response({"details": "Invalid data"}, 400) 
        
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone_number = request_body["phone"]
        return customer.make_json()
    
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return customer.return_id()

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")


@videos_bp.route("", methods= ["GET", "POST"])
def handle_videos():
    if request.method == "GET":
        videos = Video.query.all()
        get_response =[]
        for video in videos:
            get_response.append(video.make_json())

        return jsonify(get_response)
    
    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body.keys()\
            or "release_date" not in request_body.keys() \
                or "total_inventory" not in request_body.keys():
                return make_response({"details": "Invalid data"}, 400) 
        
        new_video = Video(title=request_body["title"],\
            release_date=request_body["release_date"], total_copies=request_body["total_inventory"])
        
        db.session.add(new_video)
        db.session.commit()
        return make_response(new_video.make_json(), 201)

@videos_bp.route("/<id>", methods = ["GET", "PUT", "DELETE"])
def handle_video(id):
    video = Video.query.get(id)

    if video is None:
        return make_response("", 404)

    elif request.method == "GET":
        return video.make_json()
    
    elif request.method == "PUT":
        request_body = request.get_json()

        if "title" not in request_body.keys() \
            or "release_date" not in request_body.keys() \
                or "total_inventory" not in request_body.keys():
                return make_response({"details": "Invalid data"}, 400) 
        
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_copies = request_body["total_inventory"]
        return video.make_json()
    
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return video.return_id()

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


@rentals_bp.route("/check-out", methods = ["POST"])
def rental_check_out():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    try:
        request_body["customer_id"]
        request_body["video_id"]
        customer_id in Customer.query.all()
        video_id in Video.query.all()
    except:
    # if "customer_id" not in request_body.keys() \
    #     or "video_id" not in request_body.keys():
        return make_response({"details": "Invalid data"}, 400)

    if customer is None or video is None:
        return make_response("", 404)

    # results = db.session.query(Customer, Video, Rental).join\
    #     (Customer, Customer.id==Rental.customer_id).join\
    #         (Video, Video.id==Rental.video_id).filter(Customer.id == X).all()

    elif customer.check_out() is None:
        return make_response({"details":"No copies of this video are availble"}, 400)
        
    else:
        customer.check_out()
        video.check_out()

        new_rental= Rental(due_date=(datetime.now() + timedelta(days=7)), \
                customer_id=customer_id, video_id=video_id)

        db.session.add(new_rental)
        db.session.commit()
        
        return make_response(new_rental.make_json(customer_id, video_id), 200)

@rentals_bp.route("/check-in", methods = ["POST"])
def rental_check_in():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer is None or video is None:
        return make_response("", 404)
    
    try:
        request_body["customer_id"]
        request_body["video_id"]
    except:
        return make_response({"details": "Invalid data"}, 400)
    
    returned_rental = Rental(due_date=None, customer_id=customer_id, video_id=video_id)
    
    customer.check_in()
    video.check_in()

    db.session.add(returned_rental)
    db.session.commit()
    
    return make_response(returned_rental.make_json(customer_id, video_id), 200)