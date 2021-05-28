import re
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from flask import Blueprint, request, jsonify, make_response
from app import db
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

rental_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
customer_rental_bp=Blueprint("customer_rental",__name__, url_prefix="/customers")    
video_rental_bp = Blueprint("video_rentals", __name__, url_prefix="/videos")

# POST /rentals/check-out
@rental_bp.route("/check-out", methods=["POST"])  # strict_slashes=False??
def rental_check_out():
    request_body = request.get_json()

    if "customer_id" not in request_body or "video_id" not in request_body:
        return {
            "details": f"Not found"
        }, 400

    if not isinstance(request_body["customer_id"], int):
        return {
            "details": f"Not found"
        }, 400

    customer = Customer.query.get(request_body["customer_id"])
    if customer == None:
        return {
            "details": f"Not found"
        }, 400

    if not isinstance(request_body["video_id"], int):
        return {
            "details": f"Not found"
        }, 400

    video = Video.query.get(request_body["video_id"])
    if video == None:
        return {
            "details": f"Not found"
        }, 400

    if video.total_inventory <= 0:
        return {
            "details": f"Bad Request"
        }, 400

    customer.videos_checked_out_count += 1
    video.total_inventory -= 1

    new_rental = Rental(
        customer_id= customer.customer_id,
        video_id=request_body["video_id"],
        due_date=date.today()+timedelta(days=7)
    )
    
    db.session.add(new_rental)
    db.session.commit()


    return {
        "customer_id": customer.customer_id,
        "video_id": video.video_id,
        "due_date": new_rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.total_inventory
    },200

#POST /rentals/check-in
@rental_bp.route("/check-in", methods=["POST"])  
def rental_check_in():
    request_body = request.get_json()

    customer = Customer.query.get(request_body["customer_id"])
    if customer == None:
        return make_response(f"Customer not found", 404)

    video = Video.query.get(request_body["video_id"])
    if video == None:
        return make_response(f"Video not found", 404)

    rentals = Rental.query.filter_by(customer_id=request_body["customer_id"],video_id=request_body["video_id"]).first()
    if rentals == None:
        return {
            "details": f"Bad Request"
        }, 400

    customer.videos_checked_out_count -= 1
    video.total_inventory += 1
   

    db.session.delete(rentals)
    db.session.commit()
    
    return {
            "customer_id": customer.customer_id,
            "video_id": video.video_id,
            "videos_checked_out_count": customer.videos_checked_out_count,
            "available_inventory": video.total_inventory,
        }

#GET /customers/<id>/rentals
@customer_rental_bp.route("/<int:c_id>/rentals", methods=["GET"])  # correct?
def get_customer_video_checkouts(c_id):
    rentals = Rental.query.filter_by(customer_id=c_id)
    
    rental_list = []
    for rental in rentals:
        rented_video = Video.query.get(rental.video_id)

        rental_list.append({
            "title":rented_video.title,
            "release_date":rented_video.release_date,
            "due_date":rental.due_date
        })
    return jsonify(rental_list), 200

# GET /videos/<id>/rentals
@video_rental_bp.route("/<int:v_id>/rentals", methods=["GET"])  # video_id or id?
def get_customer_current_checkouts(v_id):
#     """
#      Get all the Customers who currently have a specific Video checked out 
#     """
    customer_renters = Rental.query.filter_by(video_id=v_id)

    customers_rental_list=[]
    for customer_renter in customer_renters:
        customer = Customer.query.get(customer_renter.customer_id)

        customers_rental_list.append(
            {
                "name": customer.name,
                "due_date": customer_renter.due_date,
                "phone": customer.phone,
                "postal_code":int(customer.postal_code),
            }
            )
        return jsonify(customers_rental_list),200
