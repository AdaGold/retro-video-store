from app import db 
from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
# from app.models.rental import Rental
from datetime import datetime
import os 
# import requests



retro_video_store_bp = Blueprint("Customer",__name__)
video_bp = Blueprint("videos", __name__, url_prefix="/videos")


@retro_video_store_bp.route("/customers", methods=["GET"])
def retrieve_all_customers(): 
    customers = Customer.query.all()
    if customers is None: 
        return make_response("",200)
    else: 
        response = [customer.as_json() for customer in customers]
        return make_response(jsonify(response), 200)

@retro_video_store_bp.route("/customers", methods=["POST"])
def create_a_customer(): 
    request_body = request.get_json()

        
    for customer_attribute in ["name","postal_code","phone"]:
        if customer_attribute not in request_body:
            return jsonify(f'Missing required: {customer_attribute}'),400

     

    new_customer = Customer.from_json(request_body)
   
    db.session.add(new_customer)
    db.session.commit()


    response = {
             "id": new_customer.id 

               }
    return make_response(jsonify(response), 201)

@retro_video_store_bp.route("/customers/<customer_id>", methods=["GET","PUT","DELETE"])
def retrieve_one_customer(customer_id): 
    customer = Customer.query.filter_by(id = customer_id).first()

    if customer is None: 
        return make_response("", 404)


    if request.method == "GET":   
        return jsonify(customer.as_json()) 

    elif request.method == "PUT": 
        form_data = request.get_json()

        for customer_attribute in ["name", "postal_code","phone"]: 
            if customer_attribute not in form_data:
                return make_response(jsonify({}), 400)

        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]


        db.session.commit()

        return jsonify(customer.as_json())

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return jsonify (
        {
            "id": customer.id
        })          


        

#Routes for Videos

@video_bp.route("", methods=["GET"])
def retrieve_all_videos():
    videos = Video.query.all()
    return jsonify([
        video.to_json() for video in videos
 ])



@video_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"])
def retrieve_one_video(video_id): 
    video = Video.query.filter_by(id=video_id).first()

    if video is None: 
        return make_response("", 404)
    
    if request.method == "GET":
       return jsonify( video.to_json() 
        )

    elif request.method == "PUT": 
        form_data = request.get_json()

        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

    
        db.session.commit()
        
        return jsonify(video.to_json())

    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        
        return jsonify (
        {
            "id": video.id 
        })   

        
    
@video_bp.route("", methods=["POST"])
def create_a_video(): 
    request_body = request.get_json()

    for video_attribute in ["title", "total_inventory", "release_date"]: 
        if not (video_attribute in request_body): 
            return jsonify({}), 400 

    new_video = Video.from_json(request_body)  
    db.session.add(new_video)
    db.session.commit()


    response = {
             "id": new_video.id 

               }
    return make_response(jsonify(response), 201)
        
   

    
