from flask import Blueprint
from app import db
from flask import request, Blueprint, make_response
from flask import jsonify
import datetime
from datetime import timedelta, datetime
import requests
from flask import current_app as app
import os 
from app.models.customer import Customer
from app.models.video import Video 
from app.models.rental import Rental



# CUSTOM ENDPOINTS
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


# GET ALL CUSTOMERS *********************************************************************
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers():
    
    if request.method == "GET":  
        customers = Customer.query.all()
        customers_response = []

        for customer in customers:
            customers_response.append(customer.to_json())      
        return jsonify(customers_response)
    

# POST / CREATE NEW CUSTOMERS ***************************************************************
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customers():
    
    
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
        
    
    customer = Customer(name=request_body["name"],
                            postal_code=request_body["postal_code"],
                            phone=request_body["phone"])
    if customer.registered_at == None:
        customer.registered_at = datetime.now()

    db.session.add(customer)
    db.session.commit()

    return(
        {
            "id":customer.customer_id 
    }, 201)


# GET A SPECIFIC CUSTOMER ***********************************************************************
@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_custumer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer is None:
        return make_response({"details": "Invalid data"}, 404)
    if request.method == "GET":  
        return make_response(customer.to_json(),200)

# PUT / UPDATE A SPECIFIC CUSTOMER **************************************************************
    elif request.method == "PUT":
        
        request_body = request.get_json()
        if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)
            
        form_data = request.get_json()
        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]

        db.session.commit()
        return make_response(customer.to_json())

# DELETE A SPECIFIC CUSTOMER **********************************************************************
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
    return make_response({
        "id": customer.customer_id
    }, 200)


# GET ALL VIDEOS ------------------------------------------------------------------------------------
@videos_bp.route("", methods=["GET"], strict_slashes=False)
def videos():
    videos = Video.query.all()
    videos_response = []

    if videos is None:
        return make_response("", 404)
    for video in videos:
        videos_response.append(video.to_json())
    return jsonify(videos_response)
    
# CREATE / POST NEW VIDEOS ------------------------------------------------------------------------------
@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_videos():
    
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)
        
            
    video = Video(title=request_body["title"],
                            release_date=request_body["release_date"],
                            total_inventory=request_body["total_inventory"])
    db.session.add(video)
    db.session.commit()

    return (
        {
            "id":video.video_id 
    }, 201)


# GET A SPECIFIC VIDEO ID -----------------------------------------------------------------------------------
@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response("", 404)

    if request.method == "GET":
        return make_response(video.to_json(), 200)

# PUT / UPDATE A SPECIFIC VIDEO ID -----------------------------------------------------------------------------
    elif request.method == "PUT":      
        request_body = request.get_json()
        if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)
            
        form_data = request.get_json()
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

        db.session.commit()
        return make_response(video.to_json())

# DELETE A SPECIFIC VIDEO ID ------------------------------------------------------------------------------------
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

    return make_response({
        "id": video.video_id
    }, 200)

# HELPER FUNCTION TO SEE IF VALUE IS INTEGER---------------------------------------------------------------------
def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

# CHECK OUT A VIDEO TO A CUSTOMER +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def rent_videos():
    
    request_body = request.get_json()
    if "customer_id" not in request_body and "video_id" not in request_body: 
            return make_response(jsonify({"details": "Invalid data"}), 400)
    
    if not is_int(request_body["customer_id"]):
        return make_response(jsonify({"details": "Invalid data"}), 400)
    
    if not is_int(request_body["video_id"]):
        return make_response(jsonify({"details": "Invalid data"}), 400)

    video_id = request_body["video_id"] 
    video = Video.query.get(video_id) 
    if not video:
        return make_response(jsonify({"details": "Invalid data"}), 404) 

    if video.available_inventory <= 0:
        return make_response(jsonify({"details": "Invalid data"}), 400) 


    customer_id = request_body["customer_id"] 
    customer = Customer.query.get(customer_id) 

    if not customer:
        return make_response(jsonify({"details": "Invalid data"}), 404) 

    rental = Rental.check_out(customer_id, video_id)
    return jsonify(rental.to_json()), 200

# CHECK IN A VIDEO FROM A CUSTOMER ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def return_videos():
    
    request_body = request.get_json()
    if "customer_id" not in request_body and "video_id" not in request_body:
            return make_response(jsonify({"details": "Invalid data"}), 400)

    if not is_int(request_body["customer_id"]):
        return make_response(jsonify({"details": "Invalid data"}), 400)
    
    if not is_int(request_body["video_id"]):
        return make_response(jsonify({"details": "Invalid data"}), 400)

    video_id = request_body["video_id"]
    video = Video.query.get(video_id) 
    if not video:
        return make_response(jsonify({"details": "Invalid data"}), 404) 

    customer_id = request_body["customer_id"] 
    customer = Customer.query.get(customer_id) 

    if not customer:
        return make_response(jsonify({"details": "Invalid data"}), 404) 
        

    rental = Rental.check_in(customer_id, video_id)
    print(rental)
    if rental == None:
        return make_response(jsonify({"details": "Invalid data"}), 400)

    return jsonify(rental.to_dict()), 200

# GET RENTALS FOR SPECIFIC CUSTOMER +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def custumers_check_outs(customer_id):

    customer = Customer.query.get(customer_id)

    if Customer.query.get(customer_id) is None:
        return make_response({"details": "Invalid data"}, 404)

    rentals = db.session.query(Rental)\
        .join(Customer, Customer.customer_id==Rental.customer_id)\
        .join(Video, Video.video_id==Rental.video_id)\
        .filter(Customer.customer_id==customer_id)

    videos_rent = []
    for rental in rentals:
        video = Video.query.get(rental.video_id)
        videos_rent.append({
            "release_date":video.release_date.date().isoformat(),
            "title": video.title,
            "due_date": rental.due_date.isoformat()
        })
    return jsonify(videos_rent), 200

# GET RENTALS FOR SPECIFIC VIDEO_ID +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customer_with_rental(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return make_response({"details": "Invalid data"}, 404)

    rentals = Rental.query.filter(Rental.video_id == video_id).all()

    customers = []
    for rental in rentals:
        customer = Customer.query.get(rental.customer_id)

        if customer is None:
            continue

        customer = {
            "due_date": rental.due_date.isoformat(),
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": customer.postal_code
        }

        customers.append(customer)
    
    return jsonify(customers), 200
