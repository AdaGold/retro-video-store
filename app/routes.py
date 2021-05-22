import requests
import datetime

from sqlalchemy.sql.elements import Null
from app import db
from app.models.video import Video, Rental
from app.models.customer import Customer
from flask import json, request, Blueprint, make_response, jsonify, abort

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

# HELPER FUNCTIONS:
#=============================================================================


def valid_id_or_400(input_id):
    """
    input: an input id 
    output: a 400 status code if the input ID is not able to be converted to an integer  
    """
    # tries to convert the input_id to an integer
    try:
        return int(input_id)
    # if a ValueError is raised, return False 
    except ValueError:
        return False
        

# CUSTOMER ENDPOINTS:
#=============================================================================


@customers_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_customers():
    
    customers = Customer.query.all()
    cust_response = []

    # ❗️ would like to review why this step and why it's necessary - what does each_cust look like (what is its data type) prior to being converted to json? 
    for each_cust in customers:
        cust_response.append(each_cust.convert_to_json())

    # Note that there is no need to provide an extra clause to account for no customers because this code will just return an empty list and a 200 status code
    return jsonify(cust_response), 200




@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_single_customer(customer_id):
    

    # ❗️ Find out if get_or_404 has an optional parameter for a custom error message
    saved_customer = Customer.query.get_or_404(customer_id)

    return make_response(saved_customer.convert_to_json(), 200)



@customers_bp.route("", methods=["POST"], strict_slashes=False)
def add_new_customer():

    request_body = request.get_json()

    # ❗️ Consider refactoring into some kind of helper method 
    if (not request_body) or ("name" not in request_body) or ("postal_code" not in request_body) or ("phone" not in request_body):
        return make_response({ "details": "Invalid data"
        }, 400)

    new_customer = Customer(name=request_body["name"], 
                            postal_code=request_body["postal_code"], 
                            phone=request_body["phone"],
                            registered_at=datetime.datetime.now(tz=None))

    db.session.add(new_customer)
    db.session.commit()

    return make_response({"id": new_customer.cust_id}, 201)




@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_customer(customer_id):

    saved_customer = Customer.query.get_or_404(customer_id)

    request_body = request.get_json()

    # ❗️ Consider refactoring into some kind of helper method 
    if (not request_body) or ("name" not in request_body) or ("postal_code" not in request_body) or ("phone" not in request_body):
        return make_response({ "details": "Invalid data"
        }, 400)

    saved_customer.name = request_body["name"]
    saved_customer.postal_code = request_body["postal_code"]
    saved_customer.phone = request_body["phone"]

    db.session.commit()

    return make_response(saved_customer.convert_to_json(), 200)



    


@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(customer_id):

    saved_customer = Customer.query.get_or_404(customer_id)

    db.session.delete(saved_customer)
    db.session.commit()

    return make_response({"id": saved_customer.cust_id}, 200)




# VIDEO ENDPOINTS:
#=============================================================================

@videos_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_videos():
    
    videos = Video.query.all()
    videos_response = []

    # ❗️ would like to review why this step and why it's necessary - what does each_cust look like (what is its data type) prior to being converted to json? 
    for each_video in videos:
        videos_response.append(each_video.convert_to_json())

    # Note that there is no need to provide an extra clause to account for no customers because this code will just return an empty list and a 200 status code
    return jsonify(videos_response), 200




@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_single_video(video_id):
    

    saved_video = Video.query.get_or_404(video_id)
    # saved_video = Video.query.get(video_id)
    # if not saved_video:
    #     return make_response({ "details": "Invalid data"
    #     }, 404)

    return make_response(saved_video.convert_to_json(), 200)



@videos_bp.route("", methods=["POST"], strict_slashes=False)
def add_new_video():

    request_body = request.get_json()

    # ❗️ Consider refactoring into some kind of helper method 
    if (not request_body) or ("title" not in request_body) or ("release_date" not in request_body) or ("total_inventory" not in request_body):
        return make_response({ "details": "Invalid data"
        }, 400)

    new_video = Video(title=request_body["title"], 
                    release_date=request_body["release_date"], 
                    total_inventory=request_body["total_inventory"],
                    available_inventory=request_body["total_inventory"])

    db.session.add(new_video)
    db.session.commit()

    return make_response({"id": new_video.video_id}, 201)




@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_customer(video_id):


    # ❗️ Find out if get_or_404 has an optional parameter for a custom error message
    saved_video = Video.query.get_or_404(video_id)
    # saved_video = Video.query.get(video_id)
    # if not saved_video:
    #     return make_response({ "details": "Invalid data"
    #     }, 404)

    request_body = request.get_json()

    # ❗️ Consider refactoring into some kind of helper method 
    if (not request_body) or ("title" not in request_body) or ("release_date" not in request_body) or ("total_inventory" not in request_body):
        return make_response({ "details": "Invalid data"
        }, 400)

    saved_video.title = request_body["title"]
    saved_video.release_date = request_body["release_date"]
    saved_video.total_inventory = request_body["total_inventory"]


    db.session.commit()

    return make_response(saved_video.convert_to_json(), 200)



@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_customer(video_id):



    saved_video = Video.query.get_or_404(video_id)

    db.session.delete(saved_video)
    db.session.commit()

    return make_response({"id": saved_video.video_id}, 200)


# CUSTOM ENDPOINTS:
#=============================================================================

@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
# No route argument necessary for this endpoint
def check_out_video():

    request_body = request.get_json()

    # ❗️ just awful
    customer_id = request_body["customer_id"]
    existing_cust_id = valid_id_or_400(customer_id)
    if not existing_cust_id:
        return make_response({"details": f"Customer with id '{customer_id}' does not exist"}, 400)
    video_id = request_body["video_id"]
    existing_video_id = valid_id_or_400(video_id)
    if not existing_video_id:
        return make_response({"details": f"Video with id '{video_id}' does not exist"}, 400)


    requested_video = Video.query.get_or_404(request_body["video_id"])

    if requested_video.available_inventory == 0:
        return make_response({"Details":"The requested video is not available"}, 400)

    new_rental = Rental(fk_customer_id=request_body["customer_id"], 
                    fk_video_id=request_body["video_id"])

    # Creates a due date that is the seven days from the current date:
    new_rental.due_date = datetime.datetime.now() + datetime.timedelta(days=7)

    # Increases the customer's videos_checked_out_count by one: 
    # ❗️ This code should probably return a warning if repeat check outs are attempted on the same video_id like "did you mean to check out {movie title and id} again"
    updated_cust = Customer.query.get_or_404(new_rental.fk_customer_id)
    updated_cust.videos_checked_out_count += 1

    updated_video = Video.query.get_or_404(new_rental.fk_video_id)
    updated_video.available_inventory -= 1


    db.session.add(new_rental)
    db.session.commit()

    return make_response({ "customer_id": new_rental.fk_customer_id,
                        "video_id": new_rental.fk_video_id,
                        "due_date": new_rental.due_date,
                        "videos_checked_out_count": updated_cust.videos_checked_out_count,
                        "available_inventory": updated_video.available_inventory
                    }, 
                        200)

@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
# ❗️ may be able to combine with previous function/endpoint
def check_in_video():

    request_body = request.get_json()

    # Checks if there is even a rental record for this request, so a customer can't check a video back in twice
    video_id = request_body["video_id"]
    customer_id = request_body["customer_id"]
    rental_records = Rental.query.filter_by(fk_video_id=video_id, fk_customer_id=customer_id)
    for each_rental in rental_records:
        record_due_date = each_rental.due_date
        rental_record_id = each_rental.rental_id

    # if the record due date is None:
    if not record_due_date:
        return make_response({"details": f"Video with video id {video_id} was already checked in"}, 400)
    

    # ❗️ This code should probably return a warning if repeat check INS are attempted on the same video_id like "did you mean to check out {movie title and id} again"
    updated_cust = Customer.query.get_or_404(request_body["customer_id"])
    updated_cust.videos_checked_out_count -= 1

    updated_video = Video.query.get_or_404(request_body["video_id"])
    updated_video.available_inventory += 1

    # This was the only way I could think to mark a record in Rental to show that it had been checked back in already
    rental = Rental.query.get_or_404(rental_record_id)
    rental.due_date = None 

    # ❗️ The README doesn't say what to do with the rental record? Should it be deleted once a video gets checked back in? K yep that's what I'm gonna do 

    
    db.session.commit()

    return make_response({ "customer_id": updated_cust.cust_id,
                        "video_id": updated_video.video_id,
                        "videos_checked_out_count": updated_cust.videos_checked_out_count,
                        "available_inventory": updated_video.available_inventory
                    }, 
                        200)

    
@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customer_rentals(customer_id):



    current_rentals = []
    current_rentals_response = []

    # ❗️ concerned again about the fact that I'm not really updating the rental table at any point to indicate whether its records are current or not....
    rental_records = Rental.query.filter_by(fk_customer_id=customer_id)

    # ❗️ I know this can't be the best way to do this (might even be...the worst way), but trying to use `saved_customer.current_rentals` to get some kind of list of current rentals wasn't working in the way I expected, and I just ran out of time 
    for each_rental in rental_records:
        rental_vid_id = each_rental.fk_video_id
        rental_due_date = each_rental.due_date
        rental_id = each_rental.rental_id
        rental_info = {"vid_id": rental_vid_id, "due_date": rental_due_date, "rental_id": rental_id}
        current_rentals.append(rental_info)

    # format the response body shown in the README
    for each_video in current_rentals:
        video_info = Video.query.get_or_404(each_video["vid_id"])
        rental_info = Rental.query.get_or_404(each_video["rental_id"])
        rented_video_info = {
            "release_date": video_info.release_date,
            "title": video_info.title,
            "due_date": rental_info.due_date
        }
        current_rentals_response.append(rented_video_info)

    return jsonify(current_rentals_response), 200


@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customer_rentals(video_id):


    current_renters = []
    current_renters_response = []

    # get the rental records for this video
    rental_records = Rental.query.filter_by(fk_video_id=video_id)

    # pull the info about the customers who currently have this video checked out from the video's rental records:
    for each_rental in rental_records:
        rental_cust_id = each_rental.fk_customer_id
        rental_due_date = each_rental.due_date
        rental_id = each_rental.rental_id
        renter_info = {"customer_id": rental_cust_id, "due_date": rental_due_date, "rental_id": rental_id}
        current_renters.append(renter_info)

    # format the response body 
    for each_renter in current_renters:
        customer_info = Customer.query.get_or_404(each_renter["customer_id"])
        rental_info = Rental.query.get_or_404(each_renter["rental_id"])
        customer_renter_info = {
            "due_date": rental_info.due_date,
            "name": customer_info.name,
            "phone": customer_info.phone,
            "postal_code": customer_info.postal_code
        }
        current_renters_response.append(customer_renter_info)

    return jsonify(current_renters_response), 200




    


    
    

    
    
    
    



