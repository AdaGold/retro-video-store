from flask import Blueprint, request, make_response, jsonify
from app import db 
from app.models.customer import Customer
from app.models.video import Video
from app.models.rental import Rental
from dotenv import load_dotenv
from datetime import datetime

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")
load_dotenv()

# @customers_bp.route("", methods=["GET"], strict_slashes=False)
# def get_customers():

#     customers = Customer.query.all()
#     customers_respone = []

#     if customers is None:
#         return 404

#     for customer in customers:
#         customers_respone.append(customer.to_json_customer())

#     return jsonify(customers_respone), 200


@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def new_rental():

    # create instance of rental using customer_id and video_id
    request_body = request.get_json()
    rental = Rental(customer_id=request_body["customer_id"], video_id=request_body["video_id"], due_date=datetime.utcnow())

    # add it to database and commit 
    # db.session.add(rental)
    # db.session.commit()

    # get customer_id and create customer instance
    customer = Customer.query.get(rental.customer_id)

    # get video_id and create video instance
    video = Video.query.get(rental.video_id)

    # if customer and video exist
    if customer and video:

        # increase customer.videos_checked_out by 1
        customer.videos_checked_out += 1
    
        # decrease videos.total_inventory by 1
        if video.total_inventory != 0:
            video.total_inventory -= 1
        else:
            return {"Error": "Available inventory is not sufficient"}, 400
    
    else:
        if customer is None:
            return {"Error": "Customer does not exist"}, 404
        elif video is None:
            return {"Error": "Video does not exist"}, 404

    # add it to database and commit
    db.session.add(rental)
    db.session.commit()

    return {
        "customer_id": rental.customer_id,
        "video_id": rental.video_id,
        "due_date": rental.due_date,
        "videos_checked_out_count": customer.videos_checked_out,
        "available_inventory": video.total_inventory
    }

@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def return_rental():

    # create instance of rental using customer_id and video_id
    request_body = request.get_json()
    rental = Rental(customer_id=request_body["customer_id"], video_id=request_body["video_id"], due_date=datetime.utcnow())

    # add it to database and commit 
    # db.session.add(rental)
    # db.session.commit()

    # get customer_id and create customer instance
    customer = Customer.query.get(rental.customer_id)

    # get video_id and create video instance
    video = Video.query.get(rental.video_id)

    # if customer and video exist
    if customer and video:

        # check that rentals matches customer and video
        # rentals = Rental.query.all()

        # if request_body["customer_id"] request_body["video_id"] not in rentals:
        #     return {"Error": "Customer ID and Video ID do not match a rental"}

        # decreases customer.videos_checked_out by 1
        customer.videos_checked_out -= 1
    
        # increases videos.total_inventory by 1
        video.total_inventory += 1

    else:
        if customer is None:
            return {"Error": "Customer does not exist"}, 404
        elif video is None:
            return {"Error": "Video does not exist"}, 404

    # add it to database and commit
    db.session.commit()

    return {
        "customer_id": rental.customer_id,
        "video_id": rental.video_id,\
        "videos_checked_out_count": customer.videos_checked_out,
        "available_inventory": video.total_inventory
    }

# @customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
# def handle_customer(customer_id):

#     customer = Customer.query.get(customer_id)

#     if request.method == "GET":
#         if customer is None:
#             return make_response(f"404 Not Found", 404) 

#         else:
#             one_customer = customer.to_json_customer()

#             return jsonify(one_customer)

# @customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
# def delete_customer(customer_id):

#     customer = Customer.query.get(customer_id)

#     if customer:
#         db.session.delete(customer)
#         db.session.commit()

#         return {"id": customer.customer_id}, 200
    
#     else:
#         return make_response(f"Customer {customer_id} does not exist", 404)

# @customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
# def update_customer(customer_id):

#     customer = Customer.query.get(customer_id)
#     form_data = request.get_json()

#     if customer:
    
#         if "name" in form_data.keys() or "phone" in form_data.keys() or "postal_code" in form_data.keys():
            
#             customer.name = form_data["name"]
#             customer.phone_number = form_data["phone"]
#             customer.postal_code = form_data["postal_code"]
            
#             db.session.commit()
        
#             updated_customer = customer.to_json_customer()

#             return jsonify(updated_customer), 200
        
#         else:
#             return jsonify({"error": f"Customer {customer_id} not relevant"}), 400
    
#     else:

#         return make_response("Customer does not exist", 404)

