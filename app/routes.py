from flask import Blueprint, request, make_response, jsonify
from flask_sqlalchemy.model import Model
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
from datetime import datetime, timedelta
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@customers_bp.route("", methods=["GET"])
def get_customers():
    '''
    Gets list of all customers
    '''
    customers = Customer.query.all()

    customers_response = []
    for customer in customers:
        customers_response.append(customer.to_json())
    return jsonify(customers_response)

@customers_bp.route("", methods=["POST"])
def post_customer():
    '''
    Posts new customer
    '''
    request_body = request.get_json()

    if "name" not in request_body or "postal_code" not in request_body\
    or "phone" not in request_body:
        return ({
            "errors": ["Must input required data"]
        }, 400)
    else:
        new_customer = Customer.from_json(Customer, request_body)

        db.session.add(new_customer)
        db.session.commit()

        return {
            "id": new_customer.customer_id
        }, 201

@customers_bp.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    '''
    Gets customer by customer_id
    '''
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("No customer found", 404)

    return customer.to_json()

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    '''
    Updates specific customer information
    '''
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("No customer found", 404)

    form_data = request.get_json()
    if "name" not in form_data or "postal_code" not in form_data\
    or "phone" not in form_data:
        return ({
            "errors": ["Must input required data"]
        }, 400)

    customer.name = form_data["name"]
    customer.phone = form_data["phone"]
    customer.postal_code = form_data["postal_code"]
    customer.registered_at = datetime.utcnow()

    db.session.commit()

    return customer.to_json()

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    '''
    Deletes customer by customer_id
    '''
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("No customer found", 404)

    db.session.delete(customer)
    db.session.commit()

    return {
        "id": customer.customer_id
    }

@videos_bp.route("", methods=["GET"])
def get_videos():
    '''
    Gets list of all videos
    '''
    videos = Video.query.all()

    videos_response = []
    for video in videos:
        videos_response.append(video.to_json())
    return jsonify(videos_response)


@videos_bp.route("", methods=["POST"])
def post_video():
    '''
    Posts new video
    '''
    request_body = request.get_json()

    if "title" not in request_body or "release_date" not in request_body\
    or "total_inventory" not in request_body:
        return ({
            "errors": ["Must input required data"]
        }, 400)
    else:
        new_video = Video.from_json(Video, request_body)

        db.session.add(new_video)
        db.session.commit()

        return {
            "id": new_video.video_id
        }, 201

@videos_bp.route("/<video_id>", methods=["GET"])
def get_video(video_id):
    '''
    Gets video by video_id
    '''
    video = Video.query.get(video_id)
    if video is None:
        return make_response("No video found", 404)

    return video.to_json()

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    '''
    Updates specific video information
    '''
    video = Video.query.get(video_id)
    if video is None:
        return make_response("No video found", 404)

    form_data = request.get_json()

    video.title = form_data["title"]
    video.release_date = form_data["release_date"]
    video.total_inventory = form_data["total_inventory"]

    db.session.commit()

    return {
        "id": video.video_id,
        "title": video.title,
        "release_date": video.release_date,
        "total_inventory": video.total_inventory,
        "available_inventory": video.available_inventory
    }

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    '''
    Deletes video by video_id
    '''
    video = Video.query.get(video_id)
    if video is None:
        return make_response("No video found", 404)

    db.session.delete(video)
    db.session.commit()

    return {
        "id": video.video_id
    }

@rentals_bp.route("/check-out", methods=["POST"])
def check_out():
    '''
    Increases customer's videos_checked_out by 1
    Decreases video's available_inventory
    Creates due date 7 days from today
    '''
    request_body = request.get_json()
    # request looks like:
    # {"customer_id": 3,
    # "video_id": 1}

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if type(customer_id) != int or type(video_id) != int:
        return make_response("IDs must be an integer")

    if customer is None or video is None:
        return {
            "errors": ["Customer or video not found"]
        }, 404

    due_date = datetime.utcnow() + timedelta(days=7)

    # if video.available_inventory <= 0:
    #     return {
    #         "errors": ["There are no videos available!"]
    #     }
    new_rental = Rental(customer_id=customer_id, video_id=video_id,
    due_date=due_date)

    customer.videos_checked_out_count += 1
    video.available_inventory -= 1

    db.session.add(new_rental)
    db.session.commit()

    return {
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }

@rentals_bp.route("/check-in", methods=["POST"])
def check_in():
    '''
    Decreases customer's videos_checked_out by 1
    Increases video's available_inventory
    '''
    request_body = request.get_json()
    # request looks like:
    # {"customer_id": 3,
    # "video_id": 1}

    customer_id = request_body["customer_id"]
    video_id = request_body["video_id"]

    if type(customer_id) != int or type(video_id) != int:
        return make_response("IDs must be an integer", 400)

    customer = Customer.query.get(customer_id)
    video = Video.query.get(video_id)

    if customer is None or video is None:
        return {
            "errors": ["Customer or video not found"]
        }, 404
    # if video.available_inventory >= video.total_inventory:
    #     return {
    #         "errors": ["Did you return this to the wrong store?"]
    #     }, 400
    # if customer.videos_checked_out_count <= 0:
    #     return {
    #         "errors": ["You don't have anything to return!"]
    #     }, 400

    if customer.videos_checked_out_count <= 0:
        return make_response("", 404)
    else:
        customer.videos_checked_out_count -= 1

    if video.available_inventory <= 0:
        return make_response("", 404)
    else:
        video.available_inventory += 1

    db.session.commit()

    return {
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_customer_videos(customer_id):
    '''
    Gets list of videos a specific customer has checked out
    '''
    customer = Customer.query.get(customer_id)
    if customer is None:
        return make_response("", 404)

    video_list = [] # list of videos currently rented by customer

    rental_results = db.session.query(Customer, Video, Rental).join(
        Customer, Customer.customer_id==Rental.customer_id).join(
        Video, Video.video_id).filter(Customer.customer_id==customer_id).all()

    for tuple in rental_results:
        video = tuple[1]
        rental = tuple[2]
        video_list.append({
            "release_date": video.release_date,
            "title": video.video_title,
            "due_date": rental.due_date
        })

    return jsonify(video_list), 200

@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def get_video_customers(video_id):
    '''
    Gets list of all customers who have checked out a video
    '''
    video = Video.query.get(video_id)
    if video is None:
        return make_response("", 404)

    customer_list = [] # list of customers currently renting a video
    rental_results = db.session.query(Customer, Video, Rental).join(
        Video, Video.customer_id==Rental.customer_id).join(
        Customer, Customer.customer_id).filter(Customer.video_id==video_id).all()

    for tuple in rental_results:
        video = tuple[1]
        rental = tuple[2]
        customer_list.append({
            "release_date": video.release_date,
            "title": video.video_title,
            "due_date": rental.due_date
        })

    return jsonify(customer_list), 200

    # results = db.session.query(Customer, Rental).join(
    #     Customer, customer.customer_id==Rental.customer_id).filter(
    #     Customer.customer_id==request_body["customer_id"]).all()


# TRASH?

    # results = db.session.query(Customer, Video, Rental).join(
    #     Customer, customer.customer_id==Rental.customer_id).join(
    #     Video, video.video_id==Rental.video_id).filter(
    #     Customer.customer_id==request_body["customer_id"]).all()
    # results = list of tuples
    # look up how to extract tuples

    # Rental.query.get(customer_id)
