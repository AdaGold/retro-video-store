from flask import Blueprint
from app import db
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
from flask import jsonify
from flask import request, make_response
from datetime import datetime, timedelta
import os
import requests 


customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


def bad_request(text): 
    return ({"errors":[text]}, 400)

def customer_not_found(customer_id):
    return ({"errors":[f"Customer {customer_id} not Found"]}, 404)


@customers_bp.route("", methods=["GET"])
def get_customers_details():
    # # sudo code for optional enhancements
    # query_sort = request.args.get("sort") 
    # if query_sort == "name":
    #     query = Customer.query.order_by(Customer.name.asc())
    # pagination = query.paginate(page, per_page=10, error_out=True,)
    # # # # optional part ends
    customers = Customer.query.all()
    customers_details = []
    for customer in customers:
        customers_details.append(customer.to_json())
    return jsonify(customers_details), 200


@customers_bp.route("", methods=["POST"])
def create_customers():
    request_body = request.get_json()

    if not "name" in request_body or not request_body.get("name"):
        return bad_request("name must be provided")
    if not "postal_code" in request_body or not request_body.get("postal_code"):
        return bad_request("postal code must be provided")
    if not "phone" in request_body or not request_body.get("phone"):
        return bad_request("phone must be provided")

    new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"]
        )
    db.session.add(new_customer)
    db.session.commit()
    return ({"id":new_customer.id}, 201) 


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        return make_response(customer.to_json(), 200)
    return customer_not_found(customer_id)


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        updated_info = request.get_json()

        if not "name" in updated_info or not updated_info.get("name"):
            return bad_request("name must be provided")
        if not "postal_code" in updated_info or not updated_info.get("postal_code"):
            return bad_request("postal code must be provided")
        if not "phone" in updated_info or not updated_info.get("phone"):
            return bad_request("phone must be provided")

        customer.name = updated_info["name"]
        customer.postal_code = updated_info["postal_code"]
        customer.phone = updated_info["phone"]
        db.session.commit()
        return (customer.to_json(), 200)
    return customer_not_found(customer_id)


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return ({"id":int(customer_id)}, 200)
    return customer_not_found(customer_id)




def no_video_found(video_id):
    return ({"errors":[f"Video {video_id} not Found"]}, 404)


@videos_bp.route("", methods=["GET"])
def get_videos_details():
    videos = Video.query.all()
    videos_log = []
    for video in videos:
        videos_log.append(video.to_json())
    return jsonify(videos_log), 200


@videos_bp.route("", methods=["POST"])
def create_videos():
    request_body = request.get_json()

    if not "title" in request_body or not request_body.get("title"):
        return bad_request("must have title")
    if not "release_date" in request_body or not request_body.get("release_date"):
        return bad_request("must have release date")
    if not "total_inventory" in request_body or not request_body.get("total_inventory"):
        return bad_request("must have total inventory")

    new_video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"],
            available_inventory=request_body["total_inventory"]
        )
    db.session.add(new_video)
    db.session.commit()
    return ({"id":new_video.id}, 201) 


@videos_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    video = Video.query.get(video_id)
    if video:
        return make_response(video.to_json(), 200) 
    return no_video_found(video_id)


@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    video = Video.query.get(video_id)
    if video:
        updated_info = request.get_json()

        if not "title" in updated_info or not updated_info.get("title"): 
            return bad_request("must have title")
        if not "release_date" in updated_info or not updated_info.get("release_date"):
            return bad_request("must have release date")
        if not "total_inventory" in updated_info or not updated_info.get("total_inventory"):
            return bad_request("must have total inventory")   

        video.title = updated_info["title"]
        video.release_date = updated_info["release_date"]
        video.total_inventory = updated_info["total_inventory"]
        db.session.commit()
        return make_response(video.to_json(), 200) 
    return no_video_found(video_id)


@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    video = Video.query.get(video_id)
    if video:
        db.session.delete(video)
        db.session.commit()
        return {"id":int(video_id)}, 200
    return no_video_found(video_id)



def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False


@rentals_bp.route("/check-out", methods=["POST"])
def rental_checkout():
    request_body = request.get_json()

    if not "customer_id" in request_body or not request_body.get("customer_id") or not is_int(request_body["customer_id"]):
        return bad_request("must have cutomer id, and it must be an int")
    if not "video_id" in request_body or not request_body.get("video_id") or not is_int(request_body["video_id"]):
        return bad_request("must have video id and it must be an int")

    customer_id = request_body["customer_id"]
    customer = Customer.query.get(customer_id)
    if not customer:
        return customer_not_found(customer_id)
    video_id = request_body["video_id"]
    video = Video.query.get(video_id)
    if not video:
        return no_video_found(video_id)

    if video.available_inventory == 0:
        return bad_request("invalid data") 
    
    customer.videos_checked_out_count += 1
    video.available_inventory -= 1
    record = Rental(
            customer_id=customer_id,
            video_id=video_id,
            due_date=datetime.now() + timedelta(days=7)
        )
    db.session.add(record)
    db.session.commit()
    response = {
        "customer_id": record.customer_id,
        "video_id": record.video_id,
        "due_date": record.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
        }
    return make_response(response, 200)
    

@rentals_bp.route("/check-in", methods=["POST"])
def rental_checkin():
    request_body = request.get_json()

    if not "customer_id" in request_body or not request_body.get("customer_id"):
        return bad_request("must have customer id")
    if not "video_id" in request_body or not request_body.get("video_id"):
        return bad_request("must have video id")
    
    customer_id = request_body["customer_id"]
    customer = Customer.query.get(customer_id)
    if not customer:
        return customer_not_found(customer_id)
    video_id = request_body["video_id"]
    video = Video.query.get(video_id)
    if not video:
        return no_video_found(video_id)
    
    rental = Rental.query.filter(Rental.check_in_date == None,
                                Rental.video_id == video_id,
                                Rental.customer_id == customer_id).one_or_none()
    if not rental:
        return bad_request("invalid data")

    customer.videos_checked_out_count -= 1
    video.available_inventory += 1
    rental.check_in_date = datetime.now()
    db.session.commit()
    response = {
        "customer_id": customer_id,
        "video_id": video_id,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }
    return make_response(response, 200)



@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def customer_log(customer_id):
    renter = Customer.query.get(customer_id)
    if renter:
        rental_data = renter.rentals
        videos_log = []
        for rental in rental_data:
            videos_log.append(rental.to_json_customer())  
        return jsonify(videos_log), 200
    return customer_not_found(customer_id)


@videos_bp.route("/<video_id>/rentals", methods=["GET"])
def video_log(video_id):
    film = Video.query.get(video_id)
    if film: 
        rental_data = film.rentals 
        customer_roster = []
        for rental in rental_data: 
            customer_roster.append(rental.to_json_video())
        return jsonify(customer_roster), 200 
    return no_video_found(video_id)

