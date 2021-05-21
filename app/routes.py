import requests
import datetime
from app import db
from app.models.video import Video, Rental
from app.models.customer import Customer
from flask import request, Blueprint, make_response, jsonify, abort

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
    # if a ValueError is raised, an abort with 400 gets triggered 
    except ValueError:
        abort(400,{"message": f"ID {input_id} must be an integer", "success": False})


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
    
    valid_id_or_400(customer_id)

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

    valid_id_or_400(customer_id)

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

    valid_id_or_400(customer_id)

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
    
    valid_id_or_400(video_id)

    # ❗️ Find out if get_or_404 has an optional parameter for a custom error message
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

    valid_id_or_400(video_id)

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

    valid_id_or_400(video_id)

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

    requested_video = Video.query.get_or_404(request_body["video_id"])

    # ❗️ Make this error message more specific
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

    # ❗️ This code should probably return a warning if repeat check INS are attempted on the same video_id like "did you mean to check out {movie title and id} again"
    updated_cust = Customer.query.get_or_404(request_body["customer_id"])
    updated_cust.videos_checked_out_count -= 1

    updated_video = Video.query.get_or_404(request_body["video_id"])
    updated_video.available_inventory += 1

    # ❗️ The README doesn't say what to do with the rental record?

    db.session.commit()

    return make_response({ "customer_id": updated_cust.customer_id,
                        "video_id": updated_video.video_id,
                        "videos_checked_out_count": updated_cust.videos_checked_out_count,
                        "available_inventory": updated_video.available_inventory
                    }, 
                        200)

    
@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def get_customer_rentals(customer_id):

    valid_id_or_400(customer_id)

    # Get the customer with matching customer_id
    saved_customer = Customer.query.get_or_404(customer_id)

    # 
