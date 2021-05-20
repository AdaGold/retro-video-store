from flask import current_app, Blueprint, make_response, jsonify, request, Response
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from app import db
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

@customers_bp.route("", methods=["POST"], strict_slashes=False)
def post_customer():
    request_body = request.get_json()
    if "name" not in request_body or "postal_code" not in request_body or "phone" not in request_body:
        return make_response({
            "details": "Invalid data"
        }, 400)
    else:
        new_customer = Customer(name=request_body["name"],
                                postal_code=request_body["postal_code"],
                                phone=request_body["phone"])
        db.session.add(new_customer)
        db.session.commit()
        
        response = new_customer.return_data()

        return(make_response(response), 201)

@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_customers():
    customers = Customer.query.all()

    customers_response = []
    for customer in customers:
        customers_response.append(customer.return_data())
    
    return (make_response(jsonify(customers_response)), 200)

@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_one_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    response = customer.return_data()
    return make_response((response), 200)

@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customers_rentals(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    response= []
    for rental in customer.rentals_out:
        video = Video.query.get_or_404(rental.video_id)
        response.append(
            {"release_date": video.release_date,
            "title": video.title,
            "due_date":rental.due_date
        })
    return make_response(jsonify(response), 200)

@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    request_body = request.get_json()
    print(f"request body: {request_body}")

    if "name" not in request_body \
        or "postal_code" not in request_body \
        or "phone" not in request_body:
        return make_response({}, 400)
        
    # elif type(request_body["name"]) is not str or request_body["name"] == "" \
    #     or type(request_body["phone"]) is not str or request_body["phone"] == "" \
    #     or type(request_body["postal_code"]) is not int or request_body["postal_code"] == "":
    #     return make_response({}, 400)

    else:
        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]
        db.session.commit()

        response = customer.return_data()
        return make_response((response), 200)


@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    db.session.delete(customer)
    db.session.commit()

    response = customer.return_data()
    return make_response((response), 200)


#********************* video routes ***********************
@videos_bp.route("", methods=["POST"], strict_slashes=False)
def post_video():
    request_body = request.get_json()
    if "title" not in request_body or "release_date" not in request_body or "total_inventory" not in request_body:
        return make_response({
            "details": "Invalid data"
        }, 400)
    else:
        new_video = Video(title=request_body["title"],
                                release_date=request_body["release_date"],
                                total_inventory=request_body["total_inventory"])
        db.session.add(new_video)
        db.session.commit()
        
        response = new_video.return_data()
        return(make_response(response), 201)

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_videos():
    videos = Video.query.all()

    videos_response = []
    for video in videos:
        videos_response.append(video.return_data())
    
    return (make_response(jsonify(videos_response)), 200)


@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_one_video(video_id):
    video = Video.query.get_or_404(video_id)

    response = video.return_data()
    return make_response((response), 200)

@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customers_by_video(video_id):
    video = Video.query.get_or_404(video_id)
    response= []
    for rental in video.rentals_out:
        customer = Customer.query.get_or_404(rental.customer_id)
        response.append(
            {"due_date":rental.due_date,
            "name":customer.name,
            "phone":customer.phone,
            "postal_code": customer.postal_code
        })
    return make_response(jsonify(response), 200)

@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_video(video_id):
    video = Video.query.get_or_404(video_id)
    request_body = request.get_json()

    if "title" not in request_body \
        or "release_date" not in request_body \
        or "total_inventory" not in request_body:
        return make_response({}, 400)

#how do you make "release_date" DateTime? it looks like a string in smoke test
    # elif type(request_body["title"]) is not str or request_body["title"] == "" \
    #     or type(request_body["total_inventory"]) is not int or request_body["total_inventory"] == "" \
    #     or type(request_body["release_date"]) is not str or request_body["release_date"] == "":
    #     return make_response({}, 400)

    else:
        video.title = request_body["title"]
        video.release_date = request_body["release_date"]
        video.total_inventory = request_body["total_inventory"]
        db.session.commit()

        response = video.return_data()
        return make_response((response), 200)

@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)

    db.session.delete(video)
    db.session.commit()

    response = video.return_data()
    return make_response((response), 200)


#********************* Rental routes ***********************
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def rental_checkout():
    request_body = request.get_json()
    if type(request_body["customer_id"]) is not int or type(request_body["video_id"]) is not int:
        return make_response({
            "details": "Invalid data"
        }, 400)
    
    customer = Customer.query.get_or_404(request_body["customer_id"])  
    video = Video.query.get_or_404(request_body["video_id"]) 
    if video.available_inventory == 0:
        return make_response({
            "details": "Invalid data"
        }, 400)
    else: 
        new_rental = Rental(customer_id=request_body["customer_id"],
                            video_id=request_body["video_id"],
                            due_date= (datetime.today()+ timedelta(7)).strftime('%Y-%m-%d'),
                            )
        db.session.add(new_rental)
        customer.videos_checked_out_count += 1
        video.available_inventory -= 1
        db.session.commit()

        response = {
                "customer_id": new_rental.customer_id,
                "video_id": new_rental.video_id,
                "due_date": new_rental.due_date,
                "videos_checked_out_count": customer.videos_checked_out_count,
                "available_inventory": video.available_inventory
            }

        return(make_response(response), 200)



@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def rental_check_in():
    request_body = request.get_json()
    if not request_body["customer_id"] or not request_body["video_id"]:
        return make_response({
            "details": "Invalid data"
        }, 400)

    if type(request_body["customer_id"]) is not int \
        or type(request_body["video_id"]) is not int:
        return make_response({
            "details": "Invalid data"
        }, 400)
    else:
        customer = Customer.query.get_or_404(request_body["customer_id"])  
        video = Video.query.get_or_404(request_body["video_id"])  
        rental = Rental.query.filter_by(customer_id=request_body["customer_id"], video_id=request_body["video_id"]).first()
        if not rental:
            return make_response({
            "details": "Invalid data"
            }, 400)
        else:
            customer.videos_checked_out_count -= 1
            video.available_inventory += 1


            response = {
                    "customer_id": customer.id,
                    "video_id": video.id,
                    "videos_checked_out_count": customer.videos_checked_out_count,
                    "available_inventory": video.available_inventory
                }
            db.session.delete(rental)
            db.session.commit()
            return(make_response(response), 200)