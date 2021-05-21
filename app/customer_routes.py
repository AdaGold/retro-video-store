from re import U
from flask.wrappers import Response
from werkzeug.wrappers import ResponseStreamMixin
from app import db
from app.models.customers import Customer
from app.models.videos import Video
from app.models.rentals import Rental
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime,timedelta
import os, requests

customers_bp = Blueprint("cumtomers",__name__,url_prefix="/customers")
videos_bp = Blueprint("videos",__name__,url_prefix="/videos")
rentals_bp = Blueprint("rentals",__name__,url_prefix="/rentals")


@customers_bp.route("", methods=["POST","GET"], strict_slashes = False)
def create_customers():

    if request.method == "POST":
        request_body = request.get_json()
        
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body: 
            return ({"details":"Invalid data"},400)
        else:
            customer = Customer(name=request_body["name"],
                        phone=request_body["phone"],
                        postal_code =request_body["postal_code"],
                        registered_at= datetime.utcnow())
            db.session.add(customer)
            db.session.commit()

            return make_response(customer.to_json(),201)
    else:
        
        customers = Customer.query.all()

        customers_response = []
        for customer in customers:
                customers_response.append(customer.to_json())

        return jsonify(customers_response)


@customers_bp.route("/<int:customer_id>", methods=["GET","PUT","DELETE"], strict_slashes = False)
def a_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    
    if customer is None:
        return make_response({"details": "Invalid data"}, 404)
    
    if request.method == "GET":
        return make_response(customer.to_json(),200)

    elif request.method == "PUT":
        
        form_data = request.get_json()
        if "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data or bool(form_data) is False: 
            return ({"details":"Invalid data"},400)
        customer.name = form_data["name"]
        customer.phone = form_data["phone"]
        customer.postal_code = form_data["postal_code"]
        db.session.commit()

        return make_response(customer.to_json(),200)

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return make_response({"id":customer_id}, 200)



@videos_bp.route("", methods=["POST","GET"], strict_slashes = False)
def create_videos():

    if request.method == "POST":
        request_body = request.get_json()
        
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return ({"details":"Invalid data"},400)
        else:
            video = Video(title=request_body["title"],
                        release_date=datetime.utcnow(),
                        total_inventory =request_body["total_inventory"])
            db.session.add(video)
            db.session.commit()

            return make_response(video.video_to_json(),201)
    else:
        
        videos = Video.query.all()

        videos_response = []
        for video in videos:
                videos_response.append(video.video_to_json())

        return jsonify(videos_response)


@videos_bp.route("/<int:video_id>", methods=["GET","PUT","DELETE"], strict_slashes = False)
def a_single_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response({"details": "Invalid data"}, 404)
    
    if request.method == "GET":
        return make_response(video.video_to_json(),200)

    elif request.method == "PUT":
        form_data = request.get_json()
        if "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data or bool(form_data) is False: 
            return ({"details":"Invalid data"},400)
        video.name = form_data["title"]
        video.total_inventory = form_data["total_inventory"]
        
        db.session.commit()

        return make_response(video.video_to_json(),200)

    elif request.method == "DELETE":

        db.session.delete(video)
        db.session.commit()

        return make_response({"id":video_id}, 200)

@customers_bp.route("/<id>/rentals", methods=["GET"], strict_slashes = False)
def get_rentals_by_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return({"details":"Invalid data"},400)
    rental_list =[]
    for rental in customer.rentals:
        video = Video.query.get(rental.video_id)
        rental_list.append({
            "release_date":video.release_date,
            "title":video.title,
            "due_date":rental.due_date

        })
    return jsonify(rental_list)


@videos_bp.route("/<id>/rentals", methods=["GET"], strict_slashes = False)
def get_rentals_by_customer(id):
    video= Video.query.get(id)
    if not video:
        return({"details":"Invalid data"},400)
    rental_list =[]
    for rental in video.rentals:
        customer = Customer.query.get(rental.customer_id)
        rental_list.append({
            "name":customer.name,
            "phone":customer.phone,
            "postal_code":customer.postal_code,
            "due_date":rental.due_date

        })
    return jsonify(rental_list)


@rentals_bp.route("/check-out", methods=["POST"], strict_slashes = False)
def check_out():
    request_body = request.get_json()
    if type(request_body["customer_id"]) is not int or "customer_id" not in request_body:
        return({"details":"Invalid data"},400)
    if type(request_body["video_id"]) is not int or "video_id" not in request_body:
        return({"details":"Invalid data"},400)
    
    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])
    
    rental= Rental(
        customer_id=customer.customer_id,
        video_id=video.video_id,
        due_date=datetime.utcnow()+timedelta(days=7)
        )

    if customer is None and video is None:
        return {"error":"not found"}, 404
    
        # import pdb
        # pdb.set_trace()
    else:
        if video.available_inventory <= 0:
            return({"details":"Invalid data"},400)
        else:
            video.available_inventory -= 1
            customer.videos_checked_out_count += 1
            db.session.add(rental)
            db.session.commit()
            return rental.rental_to_json(),200
    # return make_response("",404)
    
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes = False)  
def check_in():

    request_body = request.get_json()
    
    if type(request_body["customer_id"]) is not int or type(request_body["video_id"]) is not int:
        return({"details":"Invalid data"},400) 

    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])
    rental = Rental.query.filter_by(
        customer_id = request_body["customer_id"],
        video_id = request_body["video_id"]
    ).first()
    
    if not rental:
        return({"details":"Invalid data"},400) 

    
    if rental.customer.videos_checked_out_count <=0:
        return({"details":"Invalid data"},400)
        
    rental.video.available_inventory += 1
    rental.customer.videos_checked_out_count -= 1
    db.session.commit()
    response = rental.rental_to_json()
    del response["due_date"]
    return response,200
    

