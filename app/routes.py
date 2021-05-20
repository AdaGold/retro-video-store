from flask import request,Blueprint,make_response,jsonify
from app import db
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental

from datetime import datetime
import requests
import os

customer_bp = Blueprint("customer", __name__, url_prefix="/customers")

video_bp = Blueprint("video", __name__, url_prefix="/videos")

rental_bp = Blueprint("rental", __name__, url_prefix="/rentals")

@customer_bp.route("",methods=["GET"])
def get_customers():
    name_query=request.args.get("name")
    if name_query:
        customers=Customer.query.filter_by(name=name_query)

    else:
        customers=Customer.query.all()
    
    customers_response=[]
    for customer in customers:
        customers_response.append(customer.customer_json())
    
    return jsonify(customers_response)

@customer_bp.route("",methods=["POST"])
def post_customers():
    request_body=request.get_json()
    if all(keys in request_body for keys in ("name","postal_code","phone")) == False:
        return {
            "details": "invalid data"
        }, 400
    else:
        new_customer = Customer(name=request_body["name"], postal_code=request_body["postal_code"], phone=request_body["phone"])
        db.session.add(new_customer)
        db.session.commit()

        customer=Customer.query.get(new_customer.id)
        return {
            "id": customer.id
        },201

@customer_bp.route("/<id>",methods=["GET"])
def get_customer(id):
    customer=Customer.query.get(id)

    if customer is None:
        return make_response("Customer does not exist",404)
    
    return customer.customer_json(),200


@customer_bp.route("/<id>",methods=["PUT"])
def put_customer(id):
    customer=Customer.query.get(id)
    form_data=request.get_json()
    if customer is None:
        return make_response("Customer does not exist",404)    
    
    elif all(keys in form_data for keys in ("name","postal_code","phone")) == True:
        #form_data=request.get_json()
        customer.name=form_data["name"]
        customer.postal_code=form_data["postal_code"]
        customer.phone=form_data["phone"]
        db.session.commit()

        return customer.customer_json(),200
    else:
        return make_response({"error":"Bad Request"},400)

@customer_bp.route("/<id>", methods=["DELETE"])
def delete_customer(id):
    customer=Customer.query.get(id)
    if customer is None:
        return make_response("Customer does not exist",404)    
    else:
        db.session.delete(customer)
        db.session.commit()

        return {
                "id":customer.id
        },200


@video_bp.route("",methods=["GET"])
def get_videos():
    title_query=request.args.get("title")
    if title_query:
        videos=Video.query.filter_by(title=title_query)

    else:
        videos=Video.query.all()
    
    videos_response=[]
    for video in videos:
        videos_response.append(video.video_json())
    
    return jsonify(videos_response)

@video_bp.route("",methods=["POST"])
def post_videos():
    request_body=request.get_json()
    if all(keys in request_body for keys in ("title","release_date","total_inventory")) == False:
        return {
            "details": "invalid data"
        }, 400
    else:
        new_video = Video(title=request_body["title"], release_date=request_body["release_date"], total_inventory=request_body["total_inventory"])
        db.session.add(new_video)
        db.session.commit()

        video=Video.query.get(new_video.id)
        return {
            "id": video.id
        },201

@video_bp.route("/<id>",methods=["GET"])
def get_video(id):
    video=Video.query.get(id)

    if video is None:
        return make_response("Video does not exist",404)
    
    return video.video_json(),200

@video_bp.route("/<id>",methods=["PUT"])
def put_video(id):
    video=Video.query.get(id)
    form_data=request.get_json()
    if video is None:
        return make_response("Video does not exist",404)    
    
    elif all(keys in form_data for keys in ("title","release_date","total_inventory")) == True:
        #form_data=request.get_json()
        video.title=form_data["title"]
        video.release_date=form_data["release_date"]
        video.total_inventory=form_data["total_inventory"]
        db.session.commit()

        return video.video_json(),200
    
    else:
        return make_response({"error":"Bad Request"},400)

@video_bp.route("/<id>", methods=["DELETE"])
def delete_video(id):
    video=Video.query.get(id)
    if video is None:
        return make_response("Video does not exist",404)    
    else:
        db.session.delete(video)
        db.session.commit()

        return {
                "id":video.id
        },200


@rental_bp.route("check-out",methods=["POST"])
def check_out():
    request_body=request.get_json()
    #rental_id and customer_id in request body, if not 404


    #once we retreive rental and customer id, query these in customer table, filter and checkout

    #Checking to see if video and customer exist
    if Rental.video is None or Rental.customer is None:
        return make_response(404)
    #Checking to see if request body has both keys
    elif all(keys in request_body for keys in ("customer_id","video_id")) == False:
        return make_response({"error":"Bad Request"},400)
    #Checks to see if the number of videos is more than 0 in inventory so we can rent it out
    video=Video.query.get(request_body["video_id"]).available_inventory()
    
    if video==0:
        return make_response({"error":"Bad Request"},400)
    #if all conditions are met, we return the rental status
    else:
        new_rental = Rental(customer_id=request_body["customer_id"], video_id=request_body["video_id"])
        db.session.add(new_rental)
        db.session.commit()

        #rental=Rental.query.get(new_rental.id)
        return new_rental.rental_check_out()


# results=db.session.query(Customer,Video,Rental).join(Customer,Customer.id == Rental.customer_id)\
    #         .join(Video,Video.id==Rental.video_id).filter(Customer.id==X).all() 
@rental_bp.route("check-in",methods=["POST"])
def check_in():
    # #drop due date
    # #need to return 400 if video and customer do not match rental

    request_body=request.get_json()
    if Rental.video is None or Rental.customer is None:
        return make_response(404)
    else:
        new_rental = Rental(customer_id=request_body["customer_id"], video_id=request_body["video_id"])
        db.session.add(new_rental)
        db.session.commit()

        #rental=Rental.query.get(new_rental.id)
        current_rental=new_rental.rental_check_in()
        if Rental.customer_id != current_rental["customer_id"] and Rental.video_id != current_rental["video_id"]:
            return make_response({"error":"Bad Request"},400)
        
        else:
            return current_rental
    


@video_bp.route("/<video_id>/rentals",methods=["GET"])
def current_rental_customers(video_id):
    rental_query=request.args.get(video_id)
    if rental_query:
        rentals=Rental.query.filter_by(rental=rental_query)
    else:
        rentals=Rental.query.all()
    rentals_response=[]
    for rental in rentals:
        rentals_response.append(rental.get_customer_current_rentals())
    
    return jsonify(rentals_response)


@customer_bp.route("/<customer_id>/rentals",methods=["GET"])
def current_rental_customers_by_customer(customer_id):
    rental_query=request.args.get(customer_id)
    if rental_query:
        rentals=Rental.query.filter_by(rental=rental_query)
    else:
        rentals=Rental.query.all()
    rentals_response=[]
    for rental in rentals:
        rentals_response.append(rental.get_rentals_by_customers())
    
    return jsonify(rentals_response)

# name_query=request.args.get("name")
#     if name_query:
#         customers=Customer.query.filter_by(name=name_query)

#     else:
#         customers=Customer.query.all()
    
#     customers_response=[]
#     for customer in customers:
#         customers_response.append(customer.customer_json())
    
#     return jsonify(customers_response)