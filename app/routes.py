from app import db
from flask import request, Blueprint, jsonify
from .models import Customer, Video, Rental
from datetime import datetime, timedelta


# create Blueprints:
videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False



### CRUD for CUSTOMERS  ###

# GET /customers (define a route with default empty string for GET)
@customers_bp.route("", methods=["GET"], strict_slashes=False)
def customers_index():

    customers = Customer.query.all() 

    customers_response = []

    for customer in customers:
        customers_response.append(customer.to_dict())   
    return jsonify(customers_response), 200  


# GET /customers/<id> (define a new route to GET a specific customer)
@customers_bp.route("/<customer_id>", methods=["GET"], strict_slashes=False)
def get_one_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400
    
    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404
    else:
        customer_dict = customer.to_dict()
     
    return jsonify(customer_dict), 200


# POST /customers (define a route with default empty string for POST)
@customers_bp.route("", methods=["POST"], strict_slashes=False)
def create_customer():  

    request_body = request.get_json()

    if not request_body.get("name") or not request_body.get("postal_code") \
        or not request_body.get("phone"):
        return jsonify({"details": "Invalid data"}), 400 
    
    new_customer = Customer(name = request_body["name"], \
        postal_code = request_body["postal_code"], \
            phone = request_body["phone"], \
                registered_at = datetime.now())

    db.session.add(new_customer)   
    db.session.commit()    

    customer_dict = new_customer.to_dict()

    return jsonify(customer_dict), 201


# PUT /customers/<id> (define a new route to update (PUT) one customer by its id):
@customers_bp.route("/<customer_id>", methods=["PUT"], strict_slashes=False)
def update_single_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400
    
    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404

    form_data=request.get_json()

    if not form_data.get("name") or not form_data.get("postal_code") \
        or not form_data.get("phone"):
        return jsonify({"details": "Invalid data"}), 400 

    customer.name=form_data["name"]
    customer.postal_code=form_data["postal_code"]
    customer.phone=form_data["phone"]
    db.session.commit()

    customer_dict = customer.to_dict()
    
    return jsonify(customer_dict), 200


# DELETE /customers/<id> (define a new route to DELETE one task by its id):
@customers_bp.route("/<customer_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404
   
    db.session.delete(customer)
    db.session.commit()

    return jsonify({"details": f'Customer {customer.id} "{customer.name}" successfully deleted', "id": customer.id}), 200



### CRUD for VIDEOS ###

# GET /videos
@videos_bp.route("", methods=["GET"], strict_slashes=False)
def videos_index():
    videos = Video.query.all() 

    videos_response = []

    for video in videos:
        videos_response.append(video.to_dict())   
    return jsonify(videos_response), 200 


# GET /videos/<id>
@videos_bp.route("/<video_id>", methods=["GET"], strict_slashes=False)
def get_one_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400
    
    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404
    else:
        video_dict = video.to_dict()
     
    return jsonify(video_dict), 200


# POST /videos
@videos_bp.route("", methods=["POST"], strict_slashes=False)
def create_video():  

    request_body = request.get_json()

    if not request_body.get("title") or not request_body.get("release_date") \
        or not request_body.get("total_inventory"):
        return jsonify({"details": "Invalid data"}), 400 
    
    # make new video:
    new_video = Video(title = request_body["title"], \
        release_date = request_body["release_date"], \
            total_inventory = request_body["total_inventory"], \
                available_inventory = request_body["total_inventory"])

    db.session.add(new_video)   
    db.session.commit()     

    video_dict = new_video.to_dict()

    return jsonify(video_dict), 201


# PUT /videos/<id>
@videos_bp.route("/<video_id>", methods=["PUT"], strict_slashes=False)
def update_single_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400
    
    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404

    form_data=request.get_json()

    if not form_data.get("title") or not form_data.get("release_date") \
        or not form_data.get("total_inventory"):
        return jsonify({"details": "Invalid data"}), 400 

    video.title=form_data["title"]
    video.release_date=form_data["release_date"]
    video.total_inventory=form_data["total_inventory"]
    db.session.commit()

    video_dict = video.to_dict()
    
    return jsonify(video_dict), 200


# DELETE /videos/<id>
@videos_bp.route("/<video_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400

    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404
   
    db.session.delete(video)
    db.session.commit()

    video_dict = video.to_dict()

    return jsonify(video_dict), 200



### CRUD for RENTALS ###

# POST /rentals/check-out
@rentals_bp.route("/check-out", methods=["POST"], strict_slashes=False)
def create_rental():  
    # Customer (with customer_id) rents out a specific video (with video_id), then a rental is created with an id and due date (today+7)
    request_body = request.get_json()

    if not is_int(request_body.get("customer_id")) or not is_int(request_body.get("video_id")):        
        return {"message": f"Please input an integer"}, 400

    # if request body is missing customer or video field:
    if not request_body.get("customer_id") or not request_body.get("video_id"):
        return jsonify({"details": "Invalid data"}), 400 
    
    # if customer or video does not exist:
    if request_body.get("customer_id") is None or request_body.get("video_id") is None:
        return jsonify(None), 404
    
    # get both customer_id and video_id
    customer = Customer.query.get(request_body["customer_id"])
    video = Video.query.get(request_body["video_id"])

    # If inventory check-out empty - 400
    if video.available_inventory == 0:
        return jsonify({"details": "Invalid data"}), 400 

    new_rental = Rental(customer_id = request_body["customer_id"], \
        video_id = request_body["video_id"], \
            checked_out = True)   # datetime.now() + timedelta(days=7),
                # switch the rental checked_out column to True
    
    customer.videos_checked_out_count += 1
    video.available_inventory -= 1

    db.session.add(new_rental)
    db.session.add(customer)
    db.session.add(video)  
    db.session.commit()  

    rental_dict = new_rental.to_dict()

    return jsonify(rental_dict), 200


# POST /rentals/check-in (customer (with customer_id) returns a specific video (with video_id))
@rentals_bp.route("/check-in", methods=["POST"], strict_slashes=False)
def return_rental():
    request_body = request.get_json()
    customer_id = request_body.get("customer_id")
    video_id = request_body.get("video_id")

    if not is_int(customer_id):        
        return {"message": f"Please input an integer"}, 400

    # if request body is missing customer or video field:
    if not customer_id or not video_id:
        return jsonify({"details": "Invalid data"}), 400 
    
    # if customer or video does not exist:
    if customer_id is None or video_id is None:
        return jsonify(None), 404
    
    # get both customer_id and video_id
    customer = Customer.query.get(request_body["customer_id"])  
    print(customer.customers)
    video = Video.query.get(request_body["video_id"])

    rental_id_to_upgrade = 0

    for rental in customer.customers:
        if rental.video_id == video_id and rental.checked_out == True:
            video.available_inventory += 1
            customer.videos_checked_out_count -= 1
            rental_id_to_upgrade = rental.id
            rental.checked_out = False
        else:
            return jsonify(None), 400


    rental = Rental.query.get(rental_id_to_upgrade)
    # rental = Rental.query.get(request_body["video_id"])

    # rental = Rental.query.filter(Rental.id==customer_id).filter(Rental.id==video_id).filter(Rental.status=="Checked_out").first()
    # query.filter(Rental.customer_id==customer_id).filter(Rental.video_id==video_id).filter(Rental.status=="Checked_out").first()

    ### If video and customer do not match a current rental - 400
    # if rental is None:
    #     return jsonify(None), 400

    # db.session.add(customer)
    # db.session.add(video) 
    # db.session.delete(rental) 
    db.session.commit()  

    return_dict = {
        "customer_id": request_body["customer_id"],
        "video_id": request_body["video_id"],
        "videos_checked_out_count": customer.videos_checked_out_count,
        "available_inventory": video.available_inventory
    }
    
    return jsonify(return_dict), 200 


# GET /customers/<id>/rentals (lists videos a customer currently has checked-out)
@customers_bp.route("/<customer_id>/rentals", methods=["GET"], strict_slashes=False)
def videos_rented_by_customer(customer_id):

    if not is_int(customer_id):        
        return {"message": f"ID {customer_id} must be an integer"}, 400

    customer = Customer.query.get(customer_id)

    if customer is None:
        return jsonify(None), 404

    # Get all videos associated with a customer at id customer_id
    all_videos = db.session.query(Rental).join(Customer, Customer.id==Rental.customer_id)\
            .join(Video, Video.id==Rental.video_id).filter(Customer.id == customer_id).all()
    
    all_videos_response = []
    for video in all_videos:
        all_videos_response.append({
            "title": Video.query.get(video.id).title,
            "release_date": Video.query.get(video.id).release_date,
            "due_date": video.due_date #+ timedelta(days=7)
        })
    
    return jsonify(all_videos_response), 200


# GET /videos/<id>/rentals (lists customers who currently have the video checked-out)
@videos_bp.route("/<video_id>/rentals", methods=["GET"], strict_slashes=False)
def customers_rented_video(video_id):

    if not is_int(video_id):        
        return {"message": f"ID {video_id} must be an integer"}, 400

    video = Video.query.get(video_id)

    if video is None:
        return jsonify(None), 404
    
    # Get all customers associated with a Video at id video_id
    all_rentals = db.session.query(Rental).join(Video, Video.id==Rental.video_id)\
        .join(Customer, Customer.id==Rental.customer_id).filter(Video.id==video_id).all()

    all_rentals_response = []
    for rental in all_rentals:
        customer = Customer.query.get(rental.id)
        all_rentals_response.append({
            "name": customer.name,
            "postal_code": customer.postal_code,
            "phone": customer.phone,
            "due_date": rental.due_date #+ timedelta(days=7)
        })
        # all_customers_response.append(customer.to_dict())
        
    return jsonify(all_rentals_response), 200






