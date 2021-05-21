# from app.routes import Rental_handler
from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.video import Video
# from app.models.rental import Rental
from flask import request, Blueprint, make_response
from flask import jsonify
from sqlalchemy import asc, desc
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta




customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")



# GET NEW CUSTOMERS*********************************************************************
@customers_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def get_customers():

    if request.method == "GET":
        customers = Customer.query.all() 

        customers_response = []

        for customer in customers:
            customers_response.append(customer.display_json())

        return jsonify(customers_response)

# POST / CREATE NEW CUSTOMERS****************************************************************
    elif request.method == "POST":
        request_body = request.get_json()
        if ("name" not in request_body or  "postal_code" not in request_body or "phone" not in request_body):
            return make_response(jsonify({"details": "Invalid data"}), 400)
        
        else:
            customer = Customer(name = request_body["name"],
                            postal_code = request_body["postal_code"],
                            phone = request_body["phone"])
        if customer.registered_at == None:
            customer.registered_at = datetime.datetime.now()
        

        db.session.add(customer)
        db.session.commit()


        return make_response({"id": customer.customer_id}, 201)

# GET A SPECIFIC CUSTOMER ***********************************************************************
@customers_bp.route("/<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_customer(customer_id):

    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response({"details": "invalid data"}, 404)

    if request.method == "GET":
        return make_response(customer.display_json(), 200)


# PUT / UPDATE A SPECIFIC CUSTOMER **************************************************************
    elif request.method == "PUT":
        request_body = request.get_json()
        if ("name" not in request_body or "postal_code" not in request_body or "phone" not in request_body):
            return make_response(jsonify({"details": "Invalid data"}), 400)

        form_data = request.get_json()
        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]
        db.session.commit()
        return make_response(customer.display_json())

# DELETE A SPECIFIC CUSTOMER **********************************************************************
    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()
        return make_response({"id":customer.customer_id}), 200
    


 # GET RENTALS FOR SPECIFIC CUSTOMER **********************************************************************
# @customers_bp.route("/<customer_id/rentals>", methods=["GET"], strict_slashes=False)
# def get_rentals(customer_id):

#     customer = Customer.query.get(customer_id)
#     if customer is None:
#         return make_response({"details": "invalid data"}, 404)

#     if request.method == "GET":
#         return Rental_handler.get_rentals(customer_id)



# GET VIDEOS ------------------------------------------------------------------------------------------------
@videos_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def get_videos():

    if request.method == "GET":
        videos = Video.query.all() 
    
        videos_response = []

        for video in videos:
            videos_response.append(video.display_json())

        return jsonify(videos_response)

# CREATE NEW VIDEOS -----------------------------------------------------------------------------------------
    elif request.method == "POST":
        request_body = request.get_json()
        if ("title"  not in request_body or "release_date" not in request_body or "total_inventory" not in request_body):
            return make_response(jsonify({"details": "Invalid data"}), 400)
        else:
            video = Video(title = request_body["title"],
                        release_date = datetime.fromisoformat(request_body["release_date"]),
                        total_inventory = request_body["total_inventory"])

    

        db.session.add(video)
        db.session.commit()
        return make_response({"id": video.video_id}, 201)



# GET A SPECIFIC VIDEO ID ------------------------------------------------------------------------------------
@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_video(video_id):

    video = Video.query.get(video_id)
    if video is None:
        return make_response("", 404)

    if request.method == "GET":
        return make_response(video.display_json()),200


# PUT / UPDATE A SPECIFIC VIDEO ID -----------------------------------------------------------------------------
    elif request.method == "PUT":
        request_body = request.get_json()
        if ("title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body):
            return make_response(jsonify({"details": "Invalid data"}), 400)

        form_data = request.get_json()
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]
        db.session.commit()
        return make_response(video.display_json())


# DELETE A SPECIFIC VIDEO ID ------------------------------------------------------------------------------------
    elif request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()
        return make_response({"id": video.video_id}), 200
    



# CHECK IF WE HAVE A VIDEO AVAILABLE FOR RENTAL +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# @classmethod
#     def list_rentals(cls, customer_id):
#         db_results = db.session.query(Video, Rental, Customer)\
#             .join(Rental, Rental.video_id==Video.video_id)\
#             .join(Customer, Rental.customer_id==Customer.customer_id)\
#             .filter(Customer.customer_id == customer_id).all()
#         result = []
#         for element in db_results:
#             video = element[0]
#             rental = element[1]
#             #print(element[2])
#             json = video.to_json()
#             json.pop("inventory")
#             json["due_date"] = rental.due_date
#             result.append(json)

#         return make_response(jsonify(result), 200)


# class Rental_handler():

#     @classmethod
#     def check_out(cls, data):
#         video = Video.query.get(data["video_id"])
#         rentals = Rental.query.filter_by(video_id = video.video_id).count()

#         if rentals > video.available_inventory:
#             return make_response({"Error" : "Out of stock"},400)

#         new_rental = Rental(
#             customer_id = data["customer_id"],
#             video = data["video_id"],
#             due_date = datetime.datime.now() + timedelta(days=7)
#         )

#         db.session.add(new_rental)
#         db.commit()

#         return make_response(new_rental),200