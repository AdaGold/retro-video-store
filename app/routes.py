from flask import Blueprint, request, jsonify, make_response
from app.models import customer
from app.models import video 
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental 
from datetime import datetime, time, timedelta
from app import db 
from sqlalchemy.orm import relationship, backref

#route for class Customer, Video, Rental 
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


##################################################################################
################ Wave_1 - CRUD for two models: Customer and Video ################
##################################################################################

#Post customers detail tests
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customers():

    request_body = request.get_json()

    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return jsonify({
            "errors": "Not Found"
            }), 400
    
    customer = Customer(name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
        registered_at = datetime.now())

    db.session.add(customer)
    db.session.commit()

    return jsonify({
        "id": customer.id
    }), 201

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_customers():
    customers = Customer.query.all()

    list_of_customer = []
    
    for customer in customers:
        list_of_customer.append(customer.to_json_customer())

    return jsonify(list_of_customer), 200


@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_customer_info(customer_id):

    customer = Customer.query.get(customer_id)

    if customer == None:
        return make_response({"details": "Invalid data"}, 404)

    return customer.to_json_customer(), 200

@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):

    customer = Customer.query.get(customer_id)

    if customer == None:
        return make_response({"details": "Invalid data"}, 404)

    request_body = request.get_json()

    if not "name" in request_body or not "postal_code" in request_body or not "phone" in request_body:
        return jsonify({
            "errors": "Not Found"
            }), 400
    
    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit()

    return customer.to_json_customer(), 200


@customers_bp.route("<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    
    customer = Customer.query.get(customer_id)

    if customer == None:
        return make_response({"details": "Invalid data"}, 404)

    db.session.delete(customer)
    db.session.commit()

    return jsonify({
        "id": customer.id}), 200

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_videos():

    request_body = request.get_json()

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return jsonify({
            "errors": "Not Found"
            }), 400
    
    video = Video(title= request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"],
        available_inventory = request_body['total_inventory'])

    db.session.add(video)
    db.session.commit()

    return jsonify({
        "id": video.id
    }), 201

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_video():
    videos = Video.query.all()

    list_of_video = []

    for video in videos:
        list_of_video.append(video.to_json_video())

    return jsonify(list_of_video)


@videos_bp.route("<video_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_video(video_id):
    video = Video.query.get(video_id)

    if video is None:
        return "Not Found", 404

    if request.method == "GET":
        return video.to_json_video()

    if request.method == "PUT":
        response_body_video = request.get_json()

        video.title = response_body_video["title"]
        video.release_date = response_body_video["release_date"]
        video.total_inventory = response_body_video["total_inventory"]

        return video.to_json_video()

    if request.method == "DELETE":
        db.session.delete(video)
        db.session.commit()

        return jsonify({
            "id": video.id })

##################################################################################
######### Wave_2: Custom endpoints for Rental: Many to Many relationship #########
##################################################################################

#rental checkout 
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def rental_checkout():

    rental = request.get_json()

# The API should return back detailed errors and a status 400: Bad Request if the video does not have any available inventory before check out
#check-out of invalid customer ID and video ID
    if not isinstance(rental["customer_id"], int) or not isinstance(rental["video_id"], int):
        return {
            "detail": "Invaid Data. Must be an Integer."
        }, 400

    rental_list = Rental(customer_id = rental["customer_id"],
                        video_id = rental["video_id"],
                        due_date = datetime.now() + timedelta(days=7))# adds 7 days to datetime.now(current_date)


# The API should return back detailed errors and a status 404: Not Found if the customer does not exist
    customer = Customer.query.get(rental_list.customer_id)
    if customer is None:
        return "Not Found", 404

# # The API should return back detailed errors and a status 404: Not Found if the video does not exist
    video = Video.query.get(rental_list.video_id)
    if video is None:
        return "Not Found", 404

    if video.available_inventory <= 0:
        return {
            "message": "Invalid data."
        }, 400

    customer.checkout_count += 1
    video.available_inventory -= 1


    db.session.add(rental_list)
    db.session.commit()

    return jsonify({
        "customer_id": rental_list.customer_id,
        "video_id": rental_list.video_id,
        "due_date": rental_list.due_date, #7 days from checked out date
        "videos_checked_out_count": customer.checkout_count,
        "available_inventory": video.available_inventory 
    }), 200


@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def rental_checkin():

# The API should return back detailed errors 
# and a status 400: Bad Request 
# if the video does not have any available inventory before check out

    checkin_list= request.get_json()

    checkin_customer = checkin_list["customer_id"]
    checkin_video = checkin_list["video_id"]

    customer = Customer.query.get(checkin_customer)
    video = Video.query.get(checkin_video)

    # if Customer.customer_id == checkin_customer and Video.video_id == checkin_video:
    #     return {
    #         "details": "Rental not found."
    #     }, 400

    # rental = Rental.query.all()

    if customer is None:
        return "Customer not found.", 404

    if video is None:
        return "Video not found.", 404

    rental = Rental.query.all()

    customer.checkout_count -= 1
    video.available_inventory += 1
    
    db.session.commit()

    return {
        "customer_id": customer.id,
        "video_id": video.id,
        "videos_checked_out_count": customer.checkout_count,
        "available_inventory": video.available_inventory
    }


@customers_bp.route("<customer_id>/rentals", methods=["GET"], strict_slashes=False)

# List the videos a customer currently has checked out
def get_video_by_customer_checkout(customer_id):

    customer = Customer.query.get(customer_id)

    if not customer:
        return({"details":"Invalid data"},400)
    
    print(customer)

    video_list =[]

    for rental in customer.rentals:

        video = Video.query.get(rental.video_id)

        video_list.append({
            "release_date": video.release_date,
            "title": video.title,
            "due_date": rental.due_date

        })

    return jsonify(video_list)


@videos_bp.route("<video_id>/rentals", methods=["GET"], strict_slashes=False)
# List the customers who currently have the video checked out
def get_customer_by_video_checkout(video_id):

    video= Video.query.get(video_id)

    if not video:
        return({"details":"Invalid data"},400)

    customer_list = []

    for rental in video.rentals:

        customer = Customer.query.get(rental.customer_id)

        customer_list.append({
            "name": customer.name,
            "phone": customer.phone,
            "postal_code": int(customer.postal_code),
            "due_date": rental.due_date
        })
    return jsonify(customer_list)