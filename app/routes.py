from flask import Blueprint, request, jsonify, make_response
from app.models import customer 
from app.models.customer import Customer
from app.models.video import Video
# from app.models.rental import Rental 
from datetime import datetime, time 
from app import db 

#route for class Customer 
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

# #route for class Video
# videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

#Post customers detail tests
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customers():

    request_body = request.get_json()

    if not "name" in request_body or not "postal_code" in request_body or not "phone" in request_body:
        return jsonify({
            "errors": "Not Found"
            }), 400
    
    customer = Customer(name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
        register_at = datetime.now())

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

    return jsonify(list_of_customer)


@customers_bp.route("<customer_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_customer(customer_id):

    customer = Customer.query.get(customer_id)

    # if customer is None:
    #     return make_response("", 404)

    if request.method == "GET":
        return customer.to_json_customer()

    if request.method == "PUT":
        request_body = request.get_json()

        if not "name" in request_body or not "postal_code" in request_body or not "phone" in request_body:
            return jsonify({
                "errors": "Not Found"
                }), 400

        customer.name = request_body["name"]
        customer.postal_code = request_body["postal_code"]
        customer.phone = request_body["phone"]

        db.session.commit()

        return customer.to_json_customer()

    if request.method == "DELETE":

        db.session.commit()
        # db.session.commit()

        return jsonify({
            "id": customer.id})

#route for class Video
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_videos():

    request_body = request.get_json()

    if not "title" in request_body or not "release_date" in request_body or not "total_inventory" in request_body:
        return jsonify({
            "errors": "Not Found"
            }), 400
    
    video = Video(title= request_body["title"],
        release_date = request_body["release_date"],
        total_inventory = request_body["total_inventory"])

    db.session.add(video)
    db.session.commit()

    return jsonify({
        "id": video.id
    }), 201

    # return customer.to_json_customer(), 201

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
        return make_response("", 404) 

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


#route for class rental  
# rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")


