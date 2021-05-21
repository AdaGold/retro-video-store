from app import db 
from flask import Blueprint, request, make_response, jsonify
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from datetime import datetime, timedelta
import os 
# import requests



customer_bp = Blueprint("customers",__name__,url_prefix="/customers")
video_bp = Blueprint("videos", __name__, url_prefix="/videos")
rental_bp = Blueprint("rentals",__name__, url_prefix="/rentals")


@customer_bp.route("", methods=["GET"])
def retrieve_all_customers(): 
    customers = Customer.query.all()
    if customers is None: 
        return make_response("",200)
    else: 
        response = [customer.as_json() for customer in customers]
        return make_response(jsonify(response), 200)

@customer_bp.route("", methods=["POST"])
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

@customer_bp.route("/<customer_id>", methods=["GET","PUT","DELETE"])
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
        
   


# #Routes for Rental 
@rental_bp.route("/check-out", methods=["POST"])
def rentals_check_out(): 
    request_body = request.get_json()

    for rental_attribute in ["customer_id", "video_id"]: 
        val= request_body[rental_attribute]
        if not (rental_attribute in request_body) or not isinstance(val,int): 
            return jsonify({}), 400

    customer = Customer.query.filter_by(id=request_body["customer_id"]).first()
    video = Video.query.filter_by(id=request_body["video_id"]).first()

    if customer is None or video is None:
        return jsonify(""), 404

    if video.available_inventory == 0: 
        return jsonify(""), 400

    new_check_out = Rental(video_id = request_body["video_id"],
                           customer_id = request_body ["customer_id"],
                           due_date = datetime.now() + timedelta(days=7)
    )

    
    customer.videos_checked_out_count += 1 
    video.available_inventory -= 1
    
    
    db.session.add(new_check_out)
    db.session.commit()


    response = {
                "customer_id": request_body["customer_id"],
                "video_id": request_body["video_id"],
                "due_date": new_check_out.due_date,
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory
            }

    return jsonify(response), 200
    


@rental_bp.route("/check-in", methods=["POST"])
def rentals_check_in(): 
    request_body = request.get_json()

  
    for rental_attribute in ["customer_id", "video_id"]: 
        val= request_body[rental_attribute]
        if not (rental_attribute in request_body) or not isinstance(val,int): 
            return jsonify({}), 400
        
    # foo = ["foo"]
    # foo["foo"]

    customer = Customer.query.filter_by(id=request_body["customer_id"]).first()
    video = Video.query.filter_by(id=request_body["video_id"]).first()
    rental = Rental.query.filter_by(video_id=request_body["video_id"],customer_id=request_body["customer_id"]).first()

    if customer is None or video is None:
        return jsonify(""), 404

    if rental is None: 
        return jsonify(""), 400 



    customer.videos_checked_out_count -= 1 
    video.available_inventory += 1
    
    db.session.delete(rental)
    db.session.commit()

    response = {
                "customer_id": request_body["customer_id"],
                "video_id": request_body["video_id"],
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory
            }
    
    return jsonify(response), 200
    
@customer_bp.route("/<id>/rentals", methods=["GET"])
def get_rentals_by_customer(id): 
    customer = Customer.query.filter_by(id=id).first()
    rentals = Rental.query.filter_by(customer_id=id).all()

    if not customer: 
        return ({"details": "Invalid data"}, 400)
    rental_list = []
    for rental in rentals:
        video = Video.query.filter_by(id=rental.video_id).first()
        rental_list.append({
        "release_date": video.release_date,
        "title": video.title,
        "due_date": rental.due_date

        })
    return jsonify(rental_list)

  
    
@video_bp.route("/<id>/rentals", methods=["GET"])
def get_rentals_by_customer(id): 
    video = Video.query.filter_by(id=id).first()
    rentals = Rental.query.filter_by(video_id=id).all()

    if not video: 
        return ({"details": "Invalid data"}, 400)
    rental_list = []
    for rental in rentals:
        customer = Customer.query.filter_by(id=rental.customer_id).first()
        rental_list.append({
        "name": customer.name,
        "phone": customer.phone,
        "postal_code": customer.postal_code,
        "due_date": rental.due_date

        })
    return jsonify(rental_list)







    
