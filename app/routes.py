from flask import Blueprint
from app.models.Videos import Video 
from app.models.Customers import Customer
from app.models.Rentals import Rental
from flask import Blueprint, make_response, jsonify, request
from app import db 
from sqlalchemy import asc, desc
from datetime import datetime, date, timedelta
import requests 
import os 

#blueprints 
customer_bp = Blueprint("customers", __name__, url_prefix="/customers")

video_bp = Blueprint("videos", __name__, url_prefix="/videos")

rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


#helper functions 
def make_400():
    return make_response({"Oops! Something went wrong. ": "Invalid data or format."}, 400)

def make_404():
    return make_response("Whatever you are looking for, we didn't find it.", 404)

def update_customer_from_json(body):
    pass

def get_due_date():
    due_date = date.today() + timedelta(days=7)
    return due_date

def get_rental_by_customer(customer_id):
    customer_info = db.session.query(Customer, Video, Rental).join(Customer, Customer.customer_id==Rental.customer_id)\
            .join(Video, Video.video_id==Rental.video_id).filter(Customer.customer_id == customer_id).all()
    return customer_info

def get_rental_by_video(video_id):
    video_info = db.session.query(Customer, Video, Rental).join(Customer, Customer.customer_id==Rental.customer_id)\
            .join(Video, Video.video_id==Rental.video_id).filter(Video.video_id==video_id).all()
    return video_info


#/customer endpoints 
@customer_bp.route("", methods=["GET"])
def get_all_customers():
    sort_query = request.args.get("sort")

    if sort_query:
        if sort_query == "name":
            customers = Customer.query.order_by(asc(Customer.customer_name))
        elif sort_query == "postal_code":
            customers = Customer.query.order_by(asc(Customer.customer_zip))
        elif sort_query == "registered_at":
            customers = Customer.query.order_by(asc(Customer.register_at))
        else:
            return make_400()
    else:
        customers = Customer.query.all()
    customer_response = []
    for customer in customers:
        customer_response.append(customer.to_json())    
    return jsonify(customer_response), 200

@customer_bp.route("", methods=["DELETE"])
def delete_all_customers():
    customers = Customer.query.all()
    for customer in customers:
        db.session.delete(customer)
    db.session.commit()
    return make_response("All of the customers in the database have been deleted.", 200)

@customer_bp.route("/<customer_id>", methods=["GET"])
def get_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_404()
    else:
        return make_response(customer.to_json(), 200)

@customer_bp.route("/<customer_id>", methods=["PUT"])
def update_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_404()
    else:
        request_body = request.get_json()
        try:
            customer.customer_name = request_body["name"]
            customer.customer_zip = request_body["postal_code"]
            customer.customer_phone = request_body["phone"]
        except KeyError:
            return make_400()
        db.session.commit()
        return make_response(customer.to_json(), 200)

@customer_bp.route("", methods=["POST"])
def post_new_customer():
    request_body = request.get_json()
    try:
        new_customer = Customer.new_customer_from_json(request_body)
    except KeyError:
        return make_400()
    db.session.add(new_customer)
    db.session.commit()
    return make_response({"id": new_customer.customer_id}, 201)

@customer_bp.route("/<customer_id>", methods=["DELETE"])
def delete_single_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
    else:
        return make_404()
    return make_response({"id": customer.customer_id}, 200)

@customer_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_customers_rentals(customer_id):
    customer_info = get_rental_by_customer(customer_id)
    rental_list = []
    for tuple_set in customer_info:
        video = tuple_set[1]
        rental = tuple_set[2]
        rental_list.append({
            "release_date": video.release_date, 
            "title": video.video_title, 
            "due_date": rental.due_date
            })
    return jsonify(rental_list), 200



#/video endpoints 
@video_bp.route("", methods=["GET"])
def get_all_videos():
    videos = Video.query.all()
    video_response = []
    for video in videos:
        video_response.append(video.to_json())
    return jsonify(video_response), 200

@video_bp.route("", methods=["POST"])
def create_new_video():
    request_body = request.get_json()
    try:
        new_video = Video.video_from_json(request_body)
    except KeyError:
        return make_400()
    db.session.add(new_video)
    db.session.commit()
    return make_response({"id": new_video.video_id}, 201)

@video_bp.route("/<video_id>", methods=["GET"])
def get_single_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return make_404()
    return make_response(video.to_json(), 200)

@video_bp.route("/<video_id>", methods=["PUT"])
def update_single_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return make_404()
    else:
        request_body = request.get_json()
        try:
            video.video_title = request_body["title"]
            video.release_date = request_body["release_date"]
            video.total_inventory= request_body["total_inventory"]
        except KeyError:
            return make_400()
        db.session.commit()
        return make_response(video.to_json(), 200)

@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_single_video(video_id):
    video = Video.query.get(video_id)
    if video is None:
        return make_404()
    db.session.delete(video)
    db.session.commit()
    return make_response({"id": video.video_id}, 200)

@video_bp.route("", methods=["DELETE"])
def delete_all_videos():
    videos = Video.query.all()
    for video in videos:
        db.session.delete(video)
    db.session.commit()
    return make_response("All of the videos in the database have been deleted.", 200)

@video_bp.route("/<video_id>/rentals", methods=["GET"])
def get_customers_rentals_by_video(video_id):
    video_info = get_rental_by_video(video_id)
    rental_list = []
    for tuple_set in video_info:
        customer = tuple_set[0]
        rental = tuple_set[2]
        rental_list.append({
            "name": customer.customer_name, 
            "phone": customer.customer_phone, 
            "postal_code": customer.customer_zip ,
            "due_date": rental.due_date
            })
    return jsonify(rental_list), 200


#/rental endpoints 
@rental_bp.route("", methods=["DELETE"])
def delete_all_rentals():
    all_rentals = Rental.query.all()
    for rental in all_rentals:
        db.session.delete(rental)
    db.session.commit()
    return make_response("All rental information has been deleted", 200)

@rental_bp.route("/check-out", methods=["POST"])
def check_out_video(): 
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    if type(customer_id) != int or type(video_id) != int: 
        return make_400()
    else:
        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)
    if customer is None or video is None:
        return make_404()
    if video.available_inventory == 0:
        return make_response({"Error":"We don't have any of that video in stock."}, 400)
    else:
        new_rental = Rental(customer_id=customer_id, video_id=video_id)
        customer.videos_checked_out_count += 1
        video.available_inventory -= 1
        new_rental.due_date = get_due_date()
        db.session.add(new_rental)
        db.session.commit()
    return make_response({
        "customer_id": customer.customer_id, 
        "video_id": video.video_id, 
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count, 
        "available_inventory": video.available_inventory
                            }, 200)


@rental_bp.route("/check-in", methods=["POST"])
def check_in_video():
    request_body = request.get_json()
    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]
    
    if type(customer_id) != int or type(video_id) != int: 
        return make_400()
    else:
        customer = Customer.query.get(customer_id)
        video = Video.query.get(video_id)
    if customer is None or video is None:
        return make_404()
    else:
        customer_info = get_rental_by_customer(customer_id)
        rental_list = []
        for tuple_set in customer_info:
            rental_list.append(tuple_set[2])
        if not rental_list:
            return make_400()
        for rental in rental_list:
            if video.video_id == rental.video_id:
                checked_in_rental = rental
            else:
                return make_response({"That movie isn't checked out to you"}, 400)
    customer.videos_checked_out_count -= 1
    video.available_inventory += 1 
    db.session.delete(checked_in_rental)
    db.session.commit()
    return make_response({
        "customer_id": customer.customer_id, 
        "video_id": video.video_id, 
        "videos_checked_out_count": customer.videos_checked_out_count, 
        "available_inventory": video.available_inventory
                        }, 200)



    


    
    
    
    



